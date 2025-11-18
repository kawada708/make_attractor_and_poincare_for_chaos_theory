import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 必要


# デフォルト軸ラベル
DEFAULT_X_LABEL = "K"
DEFAULT_Y_LABEL = "K + τ"
DEFAULT_Z_LABEL = "K + 2τ"

# デフォルトのポアンカレ断面 y = a x + b
DEFAULT_A = 1.0
DEFAULT_B = 0.0


def load_data(filename):
    """テキストファイルから3列データを読み込みます"""
    try:
        data = np.loadtxt(filename)
        return data
    except Exception as e:
        print("データ読み込み中にエラーが発生しました。")
        print("エラー内容:", e)
        return None


def find_poincare_section(x, y, z, a, b):
    """ポアンカレ断面 y = a x + b を通過する点を補間して求めます"""
    x_cross = []
    z_cross = []

    for i in range(len(x) - 1):
        x1 = x[i]
        x2 = x[i + 1]
        y1 = y[i]
        y2 = y[i + 1]
        z1 = z[i]
        z2 = z[i + 1]

        f1 = y1 - (a * x1 + b)
        f2 = y2 - (a * x2 + b)

        if f1 * f2 < 0.0:
            t = -f1 / (f2 - f1)
            x_new = x1 + t * (x2 - x1)
            z_new = z1 + t * (z2 - z1)

            x_cross.append(x_new)
            z_cross.append(z_new)

    return np.array(x_cross), np.array(z_cross)


def plot_attractor_and_poincare(x, y, z, x_cross, z_cross,
                                x_label, y_label, z_label,
                                a, b):
    """3Dアトラクタと2Dポアンカレマップを描画します"""
    fig = plt.figure(figsize=(12, 6))
    fig.subplots_adjust(wspace=0.25, left=0.05, right=0.95)

    # 3Dアトラクタ
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot(x, y, z, lw=0.5)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.set_zlabel(z_label)

    # 断面の枠線
    x_min = np.min(x)
    x_max = np.max(x)
    z_min = np.min(z)
    z_max = np.max(z)
    y_min = a * x_min + b
    y_max = a * x_max + b

    ax1.plot([x_min, x_max], [y_min, y_max], [z_min, z_min],
             color="red", linewidth=0.5)
    ax1.plot([x_min, x_max], [y_min, y_max], [z_max, z_max],
             color="red", linewidth=0.5)
    ax1.plot([x_min, x_min], [y_min, y_min], [z_min, z_max],
             color="red", linewidth=0.5)
    ax1.plot([x_max, x_max], [y_max, y_max], [z_min, z_max],
             color="red", linewidth=0.5)

    ax1.grid(True)

    # 2Dポアンカレマップ
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.scatter(x_cross, z_cross, s=2)
    ax2.set_xlabel(x_label)
    ax2.set_ylabel(z_label)
    ax2.grid(True)

    plt.show()


def main():
    # データファイルのパス
    print("3列データ（x, y, z）のテキストファイルのパスを入力してください。")
    file_path = input("> ").strip()

    data = load_data(file_path)
    if data is None:
        return

    if data.ndim != 2 or data.shape[1] < 3:
        print("エラー: 3列 (x, y, z) のデータが必要です。")
        return

    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]

    # 軸ラベル
    print("\n軸ラベルを設定してください（空入力 でデフォルト）。")

    x_label = input("x軸ラベル（デフォルト: " + DEFAULT_X_LABEL + "）> ").strip()
    if x_label == "":
        x_label = DEFAULT_X_LABEL

    y_label = input("y軸ラベル（デフォルト: " + DEFAULT_Y_LABEL + "）> ").strip()
    if y_label == "":
        y_label = DEFAULT_Y_LABEL

    z_label = input("z軸ラベル（デフォルト: " + DEFAULT_Z_LABEL + "）> ").strip()
    if z_label == "":
        z_label = DEFAULT_Z_LABEL

    # 断面の係数 a, b
    print("\nポアンカレ断面 y = a x + b の係数を入力してください。")
    print("空入力 で a = " + str(DEFAULT_A) + ", b = " + str(DEFAULT_B) + " を使用します。")

    params = input("a b > ").strip()
    if params == "":
        a = DEFAULT_A
        b = DEFAULT_B
    else:
        try:
            a_str, b_str = params.split()
            a = float(a_str)
            b = float(b_str)
        except:
            print("入力できなかったのでデフォルト値を使います。")
            a = DEFAULT_A
            b = DEFAULT_B

    # ポアンカレ断面を通過する点を計算
    x_cross, z_cross = find_poincare_section(x, y, z, a, b)

    print("\nポアンカレ断面を通過した点の数:", len(x_cross))

    # 描画
    plot_attractor_and_poincare(x, y, z, x_cross, z_cross,
                                x_label, y_label, z_label,
                                a, b)


if __name__ == "__main__":
    plt.rcParams["font.family"] = "Times New Roman"
    main()

