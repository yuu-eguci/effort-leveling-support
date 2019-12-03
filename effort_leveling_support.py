"""EffortLevelingSupport

tkinterを使ってるのでpython3専用。
ポケモンの努力値振りをサポートします。

以下の条件のときが対象。
    ● n体以上のポケモンにeずつ努力値を振りたい
    ● ただしパワー系アイテムが一個しかない
以下のようなことを教えてくれます
    ● 「パワーアイテムを各ポケモンに順番に持たせそれぞれ群れバトルx戦せよ」
    ● 「その後、パワーアイテムをもたせず一体戦をy戦せよ」
"""


import tkinter


def calculate(ev, num):
    """
    振りたい努力値と、同時に処理したいポケモン数を指定すると、
    パワーアイテムを各ポケモンに順番に持たせてそれぞれ群れバトルを x 回させ
    その後パワーアイテムを持たせずに単体バトルを y 回すればいいと教えてくれます。

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
    y : int
        上の説明参照
    """

    if ev <= 0 or num <= 0:
        raise ValueError(f'Invalid value, ev:{ev}, num:{num}')

    for x in range(100):
        _ = (25 * x) + (x * 5 * (num - 1))
        if _ > ev:
            x -= 1
            y = ev - ((25 * x) + (x * 5 * (num - 1)))
            return x, y


class GELS(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)

        # インスタンス変数: 入力値、振りたい努力値数。
        self.ev_value = tkinter.IntVar()
        self.ev_value.set(252)

        # インスタンス変数: 入力値、同時に処理したいポケモン数。
        self.num_value = tkinter.IntVar()
        self.num_value.set(1)

        # インスタンス変数: 結果メッセージ。
        self.result_text = tkinter.StringVar()
        self.result_text.set('The result\'s gonna be written here.')

        # Frame の外観を作ります。
        self.__create_frame_appearance()

    def __create_frame_appearance(self):
        """Frame の外観を作ります。構造は以下のとおりです。
        - Root(350x150)
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

        self.master.geometry('350x150')
        self.master.title('Green Effort Leveling Support')

        # 1段目 Frame。
        frame = tkinter.Frame(self)
        frame.pack(pady=8)

        # その中身。
        tkinter.Label(frame, text='EV').grid(
            row=0, column=0)
        tkinter.Entry(frame, width=5, textvariable=self.ev_value).grid(
            row=0, column=1)
        tkinter.Label(frame, text='to').grid(
            row=0, column=2)
        tkinter.Entry(frame, width=5, textvariable=self.num_value).grid(
            row=0, column=3)
        tkinter.Label(frame, text='pokemons').grid(
            row=0, column=4)
        tkinter.Button(frame, command=self.__on_push_button, text='Calculate!').grid(
            row=0, column=5, padx=8)

        # 2段目 Frame。
        frame_for_result = tkinter.Frame(self)
        frame_for_result.pack(pady=10)
        tkinter.Label(frame_for_result, textvariable=self.result_text).pack()

    def __on_push_button(self):
        """ボタンが押されたときのイベントです。"""

        # 計算をします。
        try:
            x, y = calculate(self.ev_value.get(), self.num_value.get())
        except ValueError:
            self.result_text.set('Please input valid numbers.')
            return

        # 結果メッセージを表示します。
        self.result_text.set('Give power-item each of them\n'
                             + f'{x} times in flock battle.\n'
                             + f'And then kick {y} pokemons\' ass')


gels = GELS()
gels.pack()
gels.mainloop()
