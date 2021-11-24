import numpy as np
import cv2
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

# テキスト描画
def putDimSpec(image, comment, ndim = -1, rate=-1):
    h, w = image.shape[:2]
    tsp = np.full((30, w), (255,), dtype=np.uint8)
    image = cv2.vconcat((image, tsp))
    if ndim == -1:
        s = comment
    else:
        s = '%s ndim=%d rate=%.2f' % (comment, ndim, rate)
    cv2.putText(image, s, (2, h+16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,),1,cv2.LINE_AA)
    return  image

# MNIST手書き数字画像の作成
def mnist_digits(instances, images_per_row=5):
    size = 28
    images_per_row = min(len(instances), images_per_row)
    images = [instance.reshape(size,size) for instance in instances]
    n_rows = (len(instances) - 1) // images_per_row + 1
    row_images = []
    n_empty = n_rows * images_per_row - len(instances)
    images.append(np.zeros((size, size * n_empty)))
    for row in range(n_rows):
        rimages = images[row * images_per_row : (row + 1) * images_per_row]
        row_images.append(np.concatenate(rimages, axis=1))
    image = np.concatenate(row_images, axis=0)
    cv2.normalize(image,image,0,255,cv2.NORM_MINMAX)
    gimage = image.astype(np.uint8)
    rimg = cv2.resize(gimage, dsize=None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return rimg

# 次元圧縮推定 次元数見積もり
def getCompressDimansions(rate, Xdata):
    pca = PCA()
    pca.fit(Xdata)

    # 寄与率 累積値計算
    cumsum = np.cumsum(pca.explained_variance_ratio_)
    d = np.argmax(cumsum >= rate) + 1
    print(d)
    return d

np.random.seed(2020)

# 手書き数字イメージ取得
mnist = fetch_openml('mnist_784', version=1)
mnist.target = mnist.target.astype(np.uint8)
X = mnist["data"]
y = mnist["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y)

rate = 0.95
#rate = 0.8

#次元圧縮推定 次元数見積もり
d = getCompressDimansions(rate, X_train)

# PCA n_components=0.95 指定
#pca095 = PCA(n_components=rate)
#X_reduced = pca095.fit_transform(X_train)           # 射影
#print('pca095 rate', rate)
#print('pca095.n_components_', pca095.n_components_)

# PCA n_components=154 指定
pca154 = PCA(n_components = d)
X_reduced = pca154.fit_transform(X_train)           # 射影
X_recovered = pca154.inverse_transform(X_reduced)   # 逆射影

# Original画像作成
g1img = mnist_digits(X_train[::2100])
g1img = putDimSpec(g1img, 'Original')

# Original画像作成
g2img = mnist_digits(X_recovered[::2100])
g2img = putDimSpec(g2img, 'Compressed', d, rate)

# 画像表示
cv2.imshow('Original', g1img)
cv2.imshow('Compressed', g2img)
cv2.waitKey(0)