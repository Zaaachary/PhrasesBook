from BookNPhrase import Phrase, Book
from tkinter import *
from tkinter.messagebox import askokcancel
from tkinter.ttk import Combobox

class BookFrame(Frame):
    """包括了书本选择的Frame 是所有涉及书本读写Frame的父类"""
    def __init__(self, parent=None, book = None, **configs):
        Frame.__init__(self, parent, **configs)
        self.book = book

    def set_book(self, book):
        self.book = book
        # self.book.open_book()


class InputForm(BookFrame):
    """输入对话框"""
    def __init__(self, parent=None, **configs):
        BookFrame.__init__(self, parent, **configs)
        self.entries = {}       # entry的字典
        self.make_widgets()

    def make_widgets(self):
        form = Frame(self)
        form.pack(expand=YES, fill=X)
        for key, value in Phrase.fieldname.items():
            row = Frame(form)
            lab = Label(row, text=value)
            ent = Entry(row)
            row.pack(side=TOP)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT)
            self.entries[key] = ent
        Button(self, text="保存或更新", command=self.save_phrase).pack(side=BOTTOM)

    def save_phrase(self):
        phrase = Phrase()
        for field in Phrase.fieldname:
            setattr(phrase, field, str(self.entries[field].get()))
        try:
            self.book.add_phrase(phrase)
        except:
            print('保存失败')


class PhraseList(BookFrame):
    """短语列表"""
    def __init__(self, parent=None, **configs):
        BookFrame.__init__(self, parent, **configs)
        self.pack(expand=YES, fill=BOTH)
        self.make_widgets()
        self.settext()
    
    def make_widgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text
    
    def settext(self, text=''):
        phrase_list = self.book.output_phrase()
        t = ''
        for phrase in phrase_list:
            t = t + phrase.en + '\t' + phrase.zh + '\n'
        self.text.delete('1.0', END)
        self.text.insert('1.0', t)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()


class PhrasesBook():
    """短语书主类"""
    def __init__(self, title='短语书'):
        self.book = Book()
        self.book.open_book()

        self.root = Tk()
        self.root.title(title)
        self.make_menubar()

        self.commonframe = Frame(self.root)
        self.make_commonframe()
        self.phraselist = None

        self.mainframe = Frame(self.root)
        self.mainframe_switch()

        self.root.mainloop()
    
    def make_menubar(self):
        # 菜单栏
        menubar = Menu(self.root)
        menubar.add_command(label='短语', command=(lambda: self.mainframe_switch('input')))
        menubar.add_command(label='列表', command=(lambda: self.mainframe_switch('list')))
        menubar.add_command(label='回顾')
        self.root.config(menu=menubar)

    def make_commonframe(self):
        # 每个页面都要显示的书选择
        Label(self.commonframe, text='Choice Book').pack(side=LEFT)
        comboxlist = Combobox(self.commonframe)
        comboxlist["values"] = self.book.search_book()
        comboxlist.current(0)
        self.phraselist = comboxlist
        comboxlist.bind("<<ComboboxSelected>>", self.choice_book(self.phraselist.get()))
        comboxlist.pack(side=LEFT)
        self.commonframe.pack()

    def choice_book(self, value):
        print(value)

    def mainframe_switch(self, mode='list'):
        """切换主要的框架中的内容"""
        self.mainframe.destroy()
        if mode == 'list':
            self.mainframe = PhraseList(self.root, book=self.book)
        elif mode == 'input':
            self.mainframe = InputForm(self.root, book=self.book)
        self.mainframe.pack()


if __name__ == "__main__":
    PB = PhrasesBook()
    
        