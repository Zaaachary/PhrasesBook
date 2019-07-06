import os
import shelve

class Phrase:
    # fieldname = {'en':'英文','zh':'中文','category':'分类'}
    fieldname = {'en':'英文','zh':'中文'}
    def __init__(self, en='phrase', zh='短语', category='未分类'):
        self.en = en
        self.zh = zh
        self.category = category

    def get_English(self):
        return self.en
    
    def get_Chinese(self):
        return self.zh
    
    def get_Category(self):
        return self.category

    def __str__(self):
        return ('<%s> : <%s>' % (self.en, self.zh))

class Book:
    def __init__(self, name='test'):
        self.name = 'books/' + name
        self.db = None
        self.quantity = 0
        self.phrases = []       # 用来存放Phrase的列表

    def open_book(self):
        try:
            # 存在文件则打开 不存在则创建
            self.db = shelve.open(self.name)
        except FileNotFoundError:
            # 找不到文件(没有books目录)
            os.system('mkdir books')
            self.db = shelve.open(self.name)
        finally:
            if 'quantity' in self.db:       # 如果书中有记录则读取    
                self.quantity = self.db['quantity']
                self.phrases = self.db['list']
            else:                           # 书中没有记录则格式化书本
                self.db['quantity'] = self.quantity
                self.db['list'] = self.phrases
                self.db.sync()

    def close_book(self):
        # 不使用书的时候调用以关闭书本
        self.db['quantity'] = self.quantity
        self.db['list'] = self.phrases
        self.db.close()

    def input_phrase_command(self):
        phrase = Phrase(en='?',zh='?')
        for field in Phrase.fieldname:
            temp = input('输入%s:' % Phrase.fieldname[field])
            setattr(phrase, field, temp)
        return phrase

    def add_phrase(self, phrase=None):
        if phrase is None:
            phrase = self.input_phrase_command()
        self.quantity += 1
        self.phrases.append(phrase)
        self.db.sync()

    def output_phrase(self, method=''):
        if method is 'command':
            print('短语书 %s 中共有 %d 个短语' % (self.name, self.quantity))
            i = 0
            for phrase in self.phrases:
                print(i, '  ', phrase)
                i += 1
        else:
            return self.phrases
            
        
    def get_phrase_by_index(self, index=0):
        return self.phrases[index]

    def update_phrase(self, index=0):
        print('要修改的是:', self.phrases[index])
        temp = input('输入回车以继续:')
        if temp is '':
            phrase = self.input_phrase_command()
            self.phrases[index] = phrase
            self.db.sync()
            print('修改成功')
        else:
            print('已取消')
        
        
if __name__ == "__main__":
    """
    创建/打开书本(输入书名)
    输入短语
    输出短语书中的所有短语
    修改某条短语
    """
    name = input('请输入书名以创建或打开短语书:')
    if name is '':
        book = Book()
    else:
        book = Book(name)

    book.open_book()
    status = 0
    while status != 3:
        print('\n0:输入新的短语:\n1:输出短语书中的所有短语\n2:修改某条短语\n3:退出')
        status = int(input('请选择:'))
        if status is 0:         # 输入新的短语
            os.system('cls')
            book.add_phrase()
            print('-'*10 + '输入成功' + '-'*10)
        elif status is 1:       # 输出所有短语
            os.system('cls')
            book.output_phrase('command')
            print('-'*10 + '输出完毕' + '-'*10)
        elif status is 2:       # 根据索引修改
            a = input('请输入你要修改的短语编号：(输入N取消)')
            if a is 'N':
                continue
            else:
                book.update_phrase(int(a))
    book.close_book()
    print('bye')