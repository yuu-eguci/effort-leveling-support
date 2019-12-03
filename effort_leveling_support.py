# coding: utf-8

'''EffortLevelingSupport

tkinterを使ってるのでpython3専用。
ポケモンの努力値振りをサポートします。

以下の条件のときが対象。
    ● n体以上のポケモンにeずつ努力値を振りたい
    ● ただしパワー系アイテムが一個しかない
以下のようなことを教えてくれます
    ● 「パワーアイテムを各ポケモンに順番に持たせそれぞれ群れバトルx戦せよ」
    ● 「その後、パワーアイテムをもたせず一体戦をy戦せよ」

'''

import tkinter


class GELS(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master.geometry('350x150')
        self.master.title('Green Effort Leveling Support')

        ev_value = tkinter.IntVar()
        ev_value.set(252)
        num_value = tkinter.IntVar()
        num_value.set(1)
        result = tkinter.StringVar()
        result.set('The result\'s gonna be written here.')

        def calculate(ev, num):
            for power in range(100):
                a = (25 * power) + (power * 5 * (num - 1))
                if a > ev:
                    power -= 1
                    rest = ev - ((25 * power) + (power * 5 * (num - 1)))
                    result.set(
                        'Give power-item each of them \n' + str(power)
                        + ' times in flock battle. \nAnd then kick '
                        + str(rest) + ' pokemons\' ass.'
                    )
                    break

        def get_value():
            if ev_value.get():
                ev = ev_value.get()
            if num_value.get():
                num = num_value.get()
            calculate(ev, num)

        frame = tkinter.Frame(self)
        frame.grid(row=0, column=0, pady=8)
        label1 = tkinter.Label(frame, text='EV')
        label1.grid(row=0, column=0)
        entry1 = tkinter.Entry(frame, width=5, textvariable=ev_value)
        entry1.grid(row=0, column=1)
        label2 = tkinter.Label(frame, text='to')
        label2.grid(row=0, column=2)
        entry2 = tkinter.Entry(frame, width=5, textvariable=num_value)
        entry2.grid(row=0, column=3)
        label3 = tkinter.Label(frame, text='pokemons')
        label3.grid(row=0, column=4)

        button = tkinter.Button(frame, command=get_value, text='Calculate!')
        button.grid(row=0, column=5, padx=8)

        frame_for_result = tkinter.Frame(self)
        frame_for_result.grid(row=1, column=0, pady=10)
        label4 = tkinter.Label(frame_for_result, textvariable=result)
        label4.pack()


if __name__ == '__main__':
    gels = GELS()
    gels.pack()
    gels.mainloop()
