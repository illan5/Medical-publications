import pandas as pd
import re


def get_data(source_path):
    return pd.read_csv(source_path, compression='gzip')


def get_authors(df):
    def standardize_author_name(auth_name):
        list_parts = auth_name.split(" ")
        main_name = list_parts[-1]
        list_parts = [part[0].upper() for part in list_parts]
        list_parts[-1] = main_name.title()
        return " ".join(list_parts)

    def format_as_df(list_authors):
        list_authors = [[" ".join(author.split(" ")[:-1]), author.split(" ")[-1]] for author in list_authors]
        return pd.DataFrame(list_authors, columns=['firstname_initial', 'lastname']).sort_values(
            by=['lastname']).reset_index(drop=True)

    df_auth = df[['authors']]
    df_auth.dropna(subset=["authors"], inplace=True)
    df_auth['authors'] = df_auth['authors'].apply(lambda x: str(x).split(','))
    df_auth['authors'] = df_auth['authors'].apply(
        lambda x: [(re.sub('[^A-Za-z0-9]+', ' ', str(author))).strip() for author in x])
    df_auth['authors'] = df_auth['authors'].apply(lambda x: [standardize_author_name(auth) for auth in x])
    auth_std_names = []
    for index, row in df_auth.iterrows():
        auth_std_names += row['authors']
    auth_std_names = set(auth_std_names)
    return format_as_df(list(auth_std_names))


def get_institutions(df):
    def valid_length(inst_name):
        if len(inst_name) > 2:
            return True
        else:
            return False

    def format_as_df(list_inst):
        return pd.DataFrame(list_inst, columns=['institution']).sort_values(by=['institution']).reset_index(drop=True)

    df_inst = df[['affiliations']]
    df_inst.dropna(subset=["affiliations"], inplace=True)
    df_inst['affiliations'] = df_inst['affiliations'].apply(lambda x: str(x).split('.,'))
    df_inst['affiliations'] = df_inst['affiliations'].apply(
        lambda x: [(re.sub('[^A-Za-z0-9]+', ' ', str(institution))).strip() for institution in x])
    institution_names = []
    for index, row in df_inst.iterrows():
        institution_names += row['affiliations']
    institution_names = list(set(institution_names))
    filtered_inst = list(filter(valid_length, institution_names))
    return format_as_df(list(filtered_inst))


if __name__ == '__main__':
    input_path = './sources/publications_min.csv.gz'
    df_data = get_data(input_path)
    df_authors = get_authors(df_data)
    df_institutions = get_institutions(df_data)

    df_authors.to_csv('./output/unique_people.csv', sep=';', index=False)
    df_institutions.to_csv('./output/unique_institutions.csv', sep=';', index=False)
    print('Finished')