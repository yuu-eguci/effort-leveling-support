"""EffortLevelingSupport

tkinterを使っています。 Python 3.15 以上で動きます。
ポケモンの努力値振りをサポートします。

以下の条件のときが対象。
    ● n体以上のポケモンにeずつ努力値を振りたい
    ● ただしパワー系アイテムが一個しかない
以下のようなことを教えてくれます
    ● 「パワーアイテムを各ポケモンに順番に持たせそれぞれ群れバトルx戦せよ」
    ● 「その後、パワーアイテムを外して群れバトルz戦、一体戦をy戦せよ」
"""

import tkinter

# 1つの能力に振れる努力値の上限です (第6世代以降) 。
MAX_EV = 252
# 学習装置で努力値が入るのは手持ちのポケモンだけです。
MAX_POKEMONS = 6


def calculate(ev, num):
    """
    振りたい努力値と、同時に処理したいポケモン数を指定すると、
    パワーアイテムを各ポケモンに順番に持たせてそれぞれ群れバトルを x 回させ
    その後パワーアイテムを外して群れバトルを z 回、単体バトルを y 回すればいいと
    教えてくれます。
    戦闘数がいちばん少なくなる組み合わせを返します。

    Parameters
    ----------
    ev : int
        振りたい努力値数
    num : int
        同時に処理したいポケモン数

    Returns
    -------
    x : int
        上の説明参照
    z : int
        上の説明参照
    y : int
        上の説明参照
    """

    if not (1 <= ev <= MAX_EV and 1 <= num <= MAX_POKEMONS):
        raise ValueError(f"Invalid value, ev:{ev}, num:{num}")

    # 群れバトル x 戦をすべてのポケモンに順番に回したときの、1体あたりの努力値です。
    # 持たせているあいだに 25 、ほかのポケモンが持っているあいだに 5 ずつ入ります。
    ev_per_x = 25 + 5 * (num - 1)
    x, rest = divmod(ev, ev_per_x)
    # 残りは、パワーアイテムなしの群れバトル (全員に 5) と
    # 単体バトル (全員に 1) で埋めます。
    z, y = divmod(rest, 5)
    return x, z, y


class GELS(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)

        # インスタンス変数: 入力値、振りたい努力値数。
        # IntVar は 2.5 を 2 に黙って切り捨てるため、文字列で受けて int() で変換します。
        self.ev_value = tkinter.StringVar()
        self.ev_value.set("252")

        # インスタンス変数: 入力値、同時に処理したいポケモン数。
        self.num_value = tkinter.StringVar()
        self.num_value.set("1")

        # インスタンス変数: 結果メッセージ。
        self.result_text = tkinter.StringVar()
        self.result_text.set("The result's gonna be written here.")

        # Frame の外観を作ります。
        self.__create_frame_appearance()

    def __create_frame_appearance(self):
        """Frame の外観を作ります。構造は以下のとおりです。
        - Root(350x170)
            - Frame
                - 1列 Label
                - 2列 Entry
                - 3列 Label
                - 4列 Entry
                - 5列 Label
                - 6列 Button
            - Frame
                - Label
        """

        self.master.geometry("350x170")
        self.master.title("Green Effort Leveling Support")

        # 1段目 Frame。
        frame = tkinter.Frame(self)
        frame.pack(pady=8)

        # その中身。
        tkinter.Label(frame, text="EV").grid(row=0, column=0)
        tkinter.Entry(frame, width=5, textvariable=self.ev_value).grid(row=0, column=1)
        tkinter.Label(frame, text="to").grid(row=0, column=2)
        tkinter.Entry(frame, width=5, textvariable=self.num_value).grid(row=0, column=3)
        tkinter.Label(frame, text="pokemons").grid(row=0, column=4)
        tkinter.Button(frame, command=self.__on_push_button, text="Calculate!").grid(
            row=0, column=5, padx=8
        )
        # Enter キーでも計算します。
        self.master.bind("<Return>", lambda _event: self.__on_push_button())

        # 2段目 Frame。
        frame_for_result = tkinter.Frame(self)
        frame_for_result.pack(pady=10)
        tkinter.Label(frame_for_result, textvariable=self.result_text).pack()

    def __on_push_button(self):
        """ボタンが押されたときのイベントです。"""

        # 計算をします。
        try:
            num = int(self.num_value.get())
            x, z, y = calculate(int(self.ev_value.get()), num)
        except ValueError:
            self.result_text.set(
                f"Please input EV 1-{MAX_EV} and pokemons 1-{MAX_POKEMONS}."
            )
            return

        # 結果メッセージを表示します。
        self.result_text.set(
            "Give power-item each of them\n"
            + f"{x} times in flock battle ({num * x} in total).\n"
            + f"Then take it away, {z} flock battles\n"
            + f"and kick {y} pokemons' ass one by one."
        )


def main():
    root = tkinter.Tk()
    gels = GELS(root)
    gels.pack()
    gels.mainloop()


if __name__ == "__main__":
    main()
