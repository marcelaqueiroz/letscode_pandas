'''Funcoes de manipulacao de dataframe'''

from IPython.display import display
import pandas as pd

def generate_stats_report(df, unwanted_stats, new_column_names):
    '''Gera o relatorio com as estatisticas do dataframe'''
    df = df.describe()
    df = df.loc[~df.index.isin(unwanted_stats)].T
    df.columns = new_column_names
    return df


def split_variables(df, unwanted_columns):
    '''Divide o dataframe em dois, com base no tipo das variaveis'''
    df_quantitative = (df
                        .loc[:, ~df.columns.isin(unwanted_columns)]
                        .select_dtypes(include='int64'))
    df_qualitative = df.select_dtypes(include='object')
    return df_quantitative, df_qualitative


def generate_frequency_report(column):
    '''Gera o relatorio com as frequencias de cada variavel qualitativa'''
    # Realiza calculos
    abs_freq = column.value_counts()  # Frequencia absoluta
    rel_freq = abs_freq / abs_freq.sum()  # Frequencia relativa
    cum_freq = rel_freq.cumsum()  # Frequencia acumulada
    rel_cum_freq = (rel_freq * 100).cumsum()  # Frequencia relativa acumulada

    # Cria o dataframe e imprime
    df = pd.DataFrame([abs_freq, cum_freq, rel_freq, rel_cum_freq]).T
    df.columns = ['F. Absoluta', 'F. Acumulada', 'F. Relativa', 'F. Relativa Acumulada']
    print(f'-----------------------------------------------------------\n\n{column.name}')
    display(df)


def to_dummy(df_qualitative, df_quantitative, qualitative_columns):
    '''
    Cria dummies para as colunas desejadas presentes em df_qualitative e junta
    com as variaveis quantitativas, retornando o dataframe resultante
    quantitativas.
    '''
    df_dummies = pd.get_dummies(df_qualitative[qualitative_columns])
    df_quantitative_dummies = (pd.concat([df_quantitative, df_dummies], axis='columns'))
    return df_quantitative_dummies
