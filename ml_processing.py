import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import data_plot_utils
import time
import utils
from sklearn.cluster import DBSCAN
from distinctipy import distinctipy


def tSNE(path_in, path_to_MEA = './raw_data/MEA_dimorphism_samples.xlsx', path_out='./merged_data5/tsne.csv',
         plots_folder='./plots_folder1'):
    utils.write_log('start tSNE')
    df_f_m_index = pd.read_excel(path_to_MEA)
    f_list, m_list = [], []
    p_list, no_p_list = [], []
    for index, row in df_f_m_index.iterrows():
        if row['female'] == 1:
            f_list.append(row.iloc[0])
        else:
            m_list.append(row.iloc[0])
        if row['parent'] == 1:
            p_list.append(row.iloc[0])
        else:
            no_p_list.append(row.iloc[0])
    df = pd.read_csv(path_in, index_col=0, header=0)
    df = df.T

    original_cols = df.columns
    df['gender'] = ''
    df['parent'] = 0
    df['labels'] = ''  # femal/male and parent/no_parent
    mapping = {0: 'male_no_parent', 1: 'male_parent', 2: 'female_no_parent', 3: 'female_parent'}
    for index, row in df.iterrows():
        id = index[-4:]
        # print(id)
        tmp = 0
        if id in f_list:
            df.at[index, 'gender'] = 'female'
            tmp += 2
        else:
            df.at[index, 'gender'] = 'male'

        if id in p_list:
            df.at[index, 'parent'] = 1
            tmp += 1

        df.at[index, 'labels'] = mapping[tmp]

    pca12 = df[['pca_feature_1', 'pca_feature_2']]
    pca12 = (pca12 - pca12.mean(axis=0) / pca12.std(axis=0))
    pca12 = 10e-4 * pca12.to_numpy()

    time_start = time.time()
    tsne = TSNE(n_components=2, init=pca12, metric='correlation', verbose=1, perplexity=60, n_iter=1500,
                early_exaggeration=20)
    tsne_pca_results = tsne.fit_transform(df[original_cols])
    # print some info regarding the tSNE
    utils.write_log(f't-SNE done! Time elapsed: {time.time()-time_start} seconds')
    df['tsne-2d-one'] = tsne_pca_results[:,0]
    df['tsne-2d-two'] = tsne_pca_results[:,1]

    # plotting and saving the tSNE
    plt.figure(figsize=(16, 10))
    sns.scatterplot(
        x="tsne-2d-one",
        y="tsne-2d-two",
        hue="labels",
        # palette=sns.color_palette("gist_heat_r", 4),
        palette=['tab:blue', 'tab:green', 'tab:orange', 'tab:red'],
        data=df,
        legend="full",
        alpha=0.3
    )
    plt.title(f't-SNE in 2d')
    data_plot_utils.save_plots(plt, f'{plots_folder}/tSNE_2d_4colors')
    plt.show()

    # plotting and saving the tSNE
    plt.figure(figsize=(16, 10))
    sns.scatterplot(
        x="tsne-2d-one",
        y="tsne-2d-two",
        hue="gender",
        palette=['tab:blue', 'tab:orange'],
        data=df,
        legend="full",
        alpha=0.3
    )
    plt.title(f't-SNE in 2d')
    data_plot_utils.save_plots(plt, f'{plots_folder}/tSNE_2d_2colors')
    plt.show()

    saved_col = [col for col in original_cols] + ['tsne-2d-one', 'tsne-2d-two']
    df_to_save = df[saved_col]  # we don't save and forward the labels col we created
    df_to_save.T.to_csv(path_out, sep=',')
    utils.write_log(f'finish tSNE. new data with the two tSNE cols is in shape {df.shape}, saved to {path_out}')


def tSNE_3d(path_in, path_to_MEA='./raw_data/MEA_dimorphism_samples.xlsx', path_out='./merged_data5/tsne.csv',
         plots_folder='./plots_folder1'):
    df_f_m_index = pd.read_excel(path_to_MEA)
    f_list, m_list = [], []
    p_list, no_p_list = [], []
    for index, row in df_f_m_index.iterrows():
        if row['female'] == 1:
            f_list.append(row.iloc[0])
        else:
            m_list.append(row.iloc[0])
        if row['parent'] == 1:
            p_list.append(row.iloc[0])
        else:
            no_p_list.append(row.iloc[0])
    df = pd.read_csv(path_in, index_col=0, header=0)
    df = df.T
    df['female'] = 0
    df['parent'] = 0
    df['category_female_parent'] = 0  # female/male += 2, parent/no_parent += 1
    for index, row in df.iterrows():
        id = index[-4:]
        if id in f_list:
            df.at[index, 'female'] = 1
            df.at[index, 'category_female_parent'] += 2
        if id in p_list:
            df.at[index, 'parent'] = 1
            df.at[index, 'category_female_parent'] += 1
    df_subset3 = df.copy()
    time_start = time.time()
    tsne_3d = TSNE(n_components=3, verbose=0, perplexity=40, n_iter=300)
    tsne_pca_results3 = tsne_3d.fit_transform(df_subset3)
    # print some info regarding the tSNE in 3d
    utils.write_log(f't-SNE in 3d done! Time elapsed: {time.time()-time_start} seconds')

    df_subset3['tsne-3d-one'] = tsne_pca_results3[:,0]
    df_subset3['tsne-3d-two'] = tsne_pca_results3[:,1]
    df_subset3['tsne-3d-three'] = tsne_pca_results3[:,2]

    ax = plt.figure(figsize=(16,10)).gca(projection='3d')
    ax.scatter(
        xs=df_subset3["tsne-3d-one"],
        ys=df_subset3["tsne-3d-two"],
        zs=df_subset3["tsne-3d-three"],
        c=df_subset3["category_female_parent"],
        cmap='Spectral',
    )
    ax.view_init(elev=20, azim=150)
    ax.set_xlabel('tsne-3d-one')
    ax.set_ylabel('tsne-3d-two')
    ax.set_zlabel('tsne-3d-three')
    plt.title(f't-SNE in 3d')
    data_plot_utils.save_plots(plt, f'{plots_folder}/tSNE_3d')
    plt.show()


def DBScan_dynm_eps(path_in, path_out, path_out_tsne_dbscan, eps_prc=70, k_neighbor=20, print_noise=True, plots_folder='./plots_folder1'):
    utils.write_log(f'start DBScan_dynm_eps: finding the best eps with eps_prc={eps_prc} and k_neighbor={k_neighbor}')
    df = pd.read_csv(path_in, index_col=0, header=0)
    df = df.T[['tsne-2d-one', 'tsne-2d-two']]
    from scipy.spatial import distance_matrix
    dist = distance_matrix(df[['tsne-2d-one', 'tsne-2d-two']], df[['tsne-2d-one', 'tsne-2d-two']])
    hist = []
    for row in dist:
        row.sort()
        hist.append(row[k_neighbor])

    chosen_eps = np.percentile(hist, eps_prc)

    sns.histplot(hist)
    plt.axvline(x=chosen_eps, color='r', linestyle='-')
    plt.title(f'The distance to the {k_neighbor}th closest neighbor.\nthe {eps_prc} quartile is {round(chosen_eps, 5)}')
    data_plot_utils.save_plots(plt, f'{plots_folder}/dbscan_choose_eps')
    plt.show()

    del df  # just close instance to save memory

    utils.write_log(f'finish DBScan_dynm_eps: found best eps is {chosen_eps}. now moving to preforming DBScan')
    DBScan(path_in, path_out, eps=chosen_eps, path_out_tsne_dbscan=path_out_tsne_dbscan, min_samples=k_neighbor,
           print_noise=print_noise, plots_folder=plots_folder)  # call the actual dbscan using the eps we found


def DBScan(path_in, path_out, path_out_tsne_dbscan, print_noise=True, plots_folder='./plots_folder1', eps=1.4, min_samples=20):
    utils.write_log('start DBScan')
    df = pd.read_csv(path_in, index_col=0, header=0)
    df = df.T

    X = df[['tsne-2d-one', 'tsne-2d-two']]
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    df['dbscan_labels'] = labels
    X['dbscan_labels'] = labels
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    utils.write_log(f'dbscan output: n_clusters_: {n_clusters_} (aka dbscan_labels) and the n_noise_: {n_noise_}')
    df_print = df.copy()
    n_clusters_print = n_clusters_+1
    if print_noise == False:
        df_print = df_print[df_print['dbscan_labels'] != -1]
        n_clusters_print -= 1

    plt.figure(figsize=(16, 10))
    sns.scatterplot(
        x="tsne-2d-one",
        y="tsne-2d-two",
        hue="dbscan_labels",
        palette=distinctipy.get_colors(n_clusters_print, pastel_factor=0.6),
        data=df_print,
        legend="full",
        alpha=0.3
    )
    plt.title(f'DBScan_eps_{round(eps, 5)} (#{n_clusters_} clusters, #{n_noise_} noise labeled as -1)')
    data_plot_utils.save_plots(plt, f'{plots_folder}/dbscan_eps_{round(eps, 5)}')
    plt.show()

    df.T.to_csv(path_out, sep=',')
    X.T.to_csv(path_out_tsne_dbscan, sep=',')
    utils.write_log(f'finish DBScan with eps {round(eps, 5)}. new data with the labels from DBScan ("dbscan_labels",'
                    f' where -1 consider noise else the given label) is in shape {df.shape}. saved to {path_out} ')


if __name__ == '__main__':
    df = pd.read_csv('./gaba_clustered_data11/gaba_dbscan.csv', index_col=0, header=0).T
    # df = pd.read_csv('./clusttered_data6/dbscan.csv', index_col=0, header=0).T
    df_print = df[df['dbscan_labels'] != -1]
    plt.figure(figsize=(16, 10))
    n_clusters_print=46
    sns.scatterplot(
        x="tsne-2d-one",
        y="tsne-2d-two",
        hue="dbscan_labels",
        palette=distinctipy.get_colors(n_clusters_print, pastel_factor=0.6),
        data=df_print,
        legend="full",
        alpha=0.3
    )
    plt.title(f'DBScan_eps_1.874 (#46 clusters)')
    # data_plot_utils.save_plots(plt, f'{plots_folder}/dbscan_eps_{round(eps, 5)}')
    plt.show()
