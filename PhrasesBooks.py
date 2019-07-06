from BookNPhrase import Phrase, Book
from tkinter import *
from tkinter.messagebox import askokcancel     # get canned std dialog

class InputForm(Frame):
    def __init__(self, parent=None, **configs):
        Frame.__init__(self, parent, **configs)
        self.entries = {}       # entry的字典
        self.make_widgets()

    def make_widgets(self):
        form = Frame(self)
        form.pack(expand=YES, fill=X)
        for field in Phrase.fieldname:
            row = Frame(form)
            lab = Label(row, text=field)
            ent = Entry(row)
            row.pack(side=TOP)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT)
            self.entries[field] = ent
        Button(self, text="保存或更新", command=self.save_phrase).pack(side=BOTTOM)

    def save_phrase(self):
        pass

class PhraseList(Frame):
    def __init__(self, parent=None, **configs):
        Frame.__init__(self, parent, **configs)
        self.pack()
        

if __name__ == "__main__":
    global book
    book = Book()
    book.open_book()

    root = Tk()
    root.title = 'PhrasesBooks'
    main_frame = InputForm(root)
    main_frame.pack()
    root.mainloop()
    
    book.close_book()