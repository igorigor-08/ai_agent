import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random


class AutoVisualizer:
    def __init__(
        self, 
        df,
        filepath,
        column_types: dict = None,
        xaxis: str = None, 
        hue: str = None,
        agg_needed: bool = None, 
    ):
        self.df = df
        self.filepath = filepath
        self.column_types = column_types
        self.xaxis = xaxis
        self.hue = hue
        self.agg_needed = agg_needed
        
        
    ### Set column_types 
    def _is_year_column(self, series):
        """Check if column is year (int, string, between 2000-2030)"""
        series_str = series.astype(str)
        if series_str.str.match(r'^(20[0-4]\d|2050)$').all():
            return True
        return False 
    def _is_datetime_column(self, series):
        """Check if column is datetime"""
        if pd.api.types.is_datetime64_any_dtype(series):
            return True
        elif pd.api.types.is_numeric_dtype(series):
            return False
        else:
            try:
                converted = pd.to_datetime(series, errors='coerce')
                if not converted.isna().all():  # At least some valid datetime
                    return True
            except (ValueError, TypeError):
                pass
        return False     
    def _infer_column_types(self):
        """
        Check column types:
            year (int/str + все значения [2000, 2050])
            numeric (int, float, ...), 
            categorical (str, category), 
            datetime (datetime), # datetime в формате числа сейчас не обрабатывается
            other (none, bool, obj, ...)
        
        returns:
            column_types: dict
        """
        column_types = {}
        for col in self.df.columns:
            if self._is_year_column(self.df[col]):
                column_types[col] = "year"
            elif self._is_datetime_column(self.df[col]):
                column_types[col] = "datetime"
            elif pd.api.types.is_numeric_dtype(self.df[col]):
                column_types[col] = "numeric"
            elif pd.api.types.is_string_dtype(self.df[col]) or pd.api.types.is_categorical_dtype(self.df[col]):
                column_types[col] = "categorical"
            else:
                try:
                    self.df[col].astype(float)
                    column_types[col] = "numeric"
                except:
                    column_types[col] = "other"
        return column_types
    
    
    ### Set xaxis and hue
    def _infer_xaxis_hue(self):
        """Decide which column is axis and which is hue"""
        year_cols = [col for col, type_ in self.column_types.items() if type_ == "year"]
        numeric_cols = [col for col, type_ in self.column_types.items() if type_ == "numeric"]
        categorical_cols = [col for col, type_ in self.column_types.items() if type_ == "categorical"]
        datetime_cols = [col for col, type_ in self.column_types.items() if type_ == "datetime"]

        if len(year_cols + datetime_cols) >= 1:
            xaxis = (year_cols + datetime_cols)[0]
            hue = categorical_cols[0] if len(categorical_cols) >= 1 else None
        elif len(categorical_cols) >= 1:
            xaxis = categorical_cols[0]
            hue = categorical_cols[1] if len(categorical_cols) > 1 else None
        elif len(numeric_cols) >= 1:
            xaxis = numeric_cols[0]
            hue = None
        else:
            raise ValueError("No valid datatypes for xaxis or hue")
        return xaxis, hue
    

    ### Set agg_needed
    def _infer_agg_needed(self):
        """Determine if aggregation is needed based on xaxis and hue"""
        if self.df.shape[1] == 1:
            return None
        if self.hue is None:
            # If xaxis has duplicate values, aggregation is needed
            return self.df[self.xaxis].nunique() != self.df.shape[0]
        else:
            # If the combination of xaxis and hue has duplicate values, aggregation is needed
            return self.df[[self.xaxis, self.hue]].drop_duplicates().shape[0] != self.df.shape[0] 
    
    
    ### Run visualization
    def visualize(self):
        """
        Decide the best visualization based on column types and data

        returns:
            df
            fig
        """
        self.column_types = self._infer_column_types()
        self.xaxis, self.hue = self._infer_xaxis_hue()
        self.agg_needed = self._infer_agg_needed()

        year_cols = [col for col, type_ in self.column_types.items() if type_ == "year"]
        numeric_cols = [col for col, type_ in self.column_types.items() if type_ == "numeric"]
        categorical_cols = [col for col, type_ in self.column_types.items() if type_ == "categorical"]
        datetime_cols = [col for col, type_ in self.column_types.items() if type_ == "datetime"]

        if self.df.shape[0] == 0:
            return None, None
        elif self.df.shape == (1, 1):
            return self.df, None
        elif len(numeric_cols) == 0:
            return self.df, None

        
        # Set a consistent color palette
        sns.set_palette("husl")        
        if self.agg_needed:
            # Box plot 
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
            if self.hue is None:
                sns.boxplot(x=self.df[self.xaxis], y=self.df[numeric_cols[0]], ax=ax)
            else:
                sns.boxplot(x=self.df[self.xaxis], y=self.df[numeric_cols[0]], hue=self.df[self.hue], ax=ax)
            ax.set_title(f'{numeric_cols[0]} {self.hue}', fontsize=16)
            ax.set_ylabel('Value', fontsize=14)
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.show()
            
        else:
            if len(year_cols + datetime_cols) == 0 and len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
                # Bar plot for categorical vs numeric data
                fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
                sns.barplot(data=self.df, x=categorical_cols[0], y=numeric_cols[0], hue=self.hue, ax=ax)
                ax.set_xlabel(categorical_cols[0], fontsize=14)
                ax.set_ylabel(numeric_cols[0], fontsize=14)
                ax.set_title(f'{numeric_cols[0]} by {categorical_cols[0]}', fontsize=16)
                ax.grid(True, linestyle='--', alpha=0.6)
                plt.xticks(rotation=45, fontsize=12)
                plt.yticks(fontsize=12)
                plt.legend(fontsize=12)
                plt.tight_layout()
                plt.show()

            elif len(year_cols + datetime_cols) >= 1 and len(numeric_cols) >= 1:
                # Line plot for time series data
                self.df = self.df.sort_values(self.xaxis)
                fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
                if self.hue is None:
                    for i in numeric_cols:
                        ax.plot(self.df[self.xaxis], self.df[i], '-o', label=i, linewidth=2.5)
                    ax.set_xlabel(self.xaxis, fontsize=14)
                    ax.set_ylabel('Value', fontsize=14)
                    ax.set_title(f'{numeric_cols} over {self.xaxis}', fontsize=16)
                else:
                    for j in self.df[self.hue].unique():
                        for i in numeric_cols:
                            ax.plot(self.df[self.df[self.hue] == j][self.xaxis], 
                                    self.df[self.df[self.hue] == j][i],
                                    '-o',
                                    label=f'{i} {j}', linewidth=2.5)
                    ax.set_xlabel(self.xaxis, fontsize=14)
                    ax.set_ylabel('Value', fontsize=14)
                    ax.set_title(f'{numeric_cols} over {self.xaxis} by {self.hue}', fontsize=16)
                ax.grid(True, linestyle='--', alpha=0.6)
                plt.xticks(rotation=45, fontsize=12)
                plt.yticks(fontsize=12)
                plt.legend(fontsize=12)
                plt.tight_layout()
                plt.show()

            if self.df.shape[1] == 1:
                # Box plot for single numeric column
                fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
                sns.boxplot(data=self.df[numeric_cols[0]], ax=ax)
                ax.set_xticks([])
                ax.set_title(numeric_cols[0], fontsize=16)
                ax.set_ylabel('Value', fontsize=14)
                ax.grid(True, linestyle='--', alpha=0.6)
                plt.tight_layout()
                plt.show()

            elif self.column_types[self.xaxis] == 'numeric':
                # Scatter plot for numeric vs numeric data with marginal distributions
                joint_grid = sns.jointplot(data=self.df, x=numeric_cols[0], y=numeric_cols[1], kind='kde', height=8)
                joint_grid.ax_joint.set_xlabel(numeric_cols[0], fontsize=14)
                joint_grid.ax_joint.set_ylabel(numeric_cols[1], fontsize=14)
                joint_grid.ax_joint.set_title(f'{numeric_cols[1]} vs {numeric_cols[0]}', fontsize=16)
                joint_grid.ax_joint.grid(True, linestyle='--', alpha=0.6)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=12)
                plt.tight_layout()
                plt.show()
        plt.savefig(self.filepath)
        return self.df, True


def dataframe_to_html_table(df, **kwargs):

    default_options = {
        'index': False,
        'escape': True,
        'border': 1,
        'classes': ['table', 'table-striped', 'table-hover'],
        'na_rep': 'N/A'
    }
    
    options = {**default_options, **kwargs}
    
    html = df.to_html(**options)
    
    styled_html = f"""
    <div style="overflow-x: auto;">
        {html}
    </div>
    """
    
    return styled_html