from tkinter import *
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import configparser, os, webbrowser, sys

class TextEdit:
  _textFilename = ''
  _defaultEncoding = sys.getdefaultencoding()
  _encoding = sys.getdefaultencoding()

  @property
  def textFilename(self):
    return self._textFilename

  @textFilename.setter
  def textFilename(self, value):
    self._textFilename = value

    if value == '':
      root.title(self.__class__.__name__)
      self.menuFile.entryconfigure('保存', state=DISABLED)
    else:
      root.title(os.path.basename(value))
      self.menuFile.entryconfigure('保存', state=NORMAL)
      self.directory = os.path.dirname(value)

  def __init__(self, root):
    self.text = ScrolledText(root, bd=-3, padx=10, pady=10)
    self.text.pack(expand=1, fill=BOTH)
    self.fileTypes = [('テキストファイル', '*.txt'), ('すべてのファイル','*.*')]
    self.directory = os.path.expanduser('~')

    clientHeight = '500'
    clientWidth = '500'
    cp = configparser.ConfigParser()
    try:
      cp.read(self.__class__.__name__ + '.ini')
      clientHeight = cp['Client']['Height']
      clientWidth = cp['Client']['Width']
      self.directory = cp['File']['Directory']
    except:
      print(self.__class__.__name__ + ':Use default value(s)', file=sys.stderr)
    root.geometry(clientWidth + 'x' + clientHeight)
    root.protocol('WM_DELETE_WINDOW', self.menuFileExit)

    root.option_add('*tearOff', FALSE)
    self.createMenu()
    self.menuFileNew()

  def createMenu(self):
    menu = Menu(root)
    self.menuFile = Menu(menu)
    menu.add_cascade(menu=self.menuFile, label='ファイル', underline=5)
    self.menuFile.add_command(label='新規ファイル', underline=3, accelerator='Command+N', command=self.menuFileNew)
    self.menuFile.add_command(label='開く...', underline=3, accelerator='Command+O', command=self.menuFileOpen)
    self.menuFile.add_command(label='保存', underline=3, accelerator='Command+S', command=self.menuFileSave)
    self.menuFile.add_command(label='名前を付けて保存', underline=3, accelerator='Command+Shift+S', command=self.fileSaveAs)
    self.menuFile.add_separator()
    self.menuFile.add_command(label='終了', underline=3, accelerator='Command+Shift+W', command=self.menuFileExit)

    menuHelp = Menu(menu)
    menu.add_cascade(menu=menuHelp, label='ヘルプ', underline=4)
    menuHelp.add_command(label='リリースノート', underline=10, command=self.menuHelpOpenReleaseNotes)
    menuHelp.add_separator()
    menuHelp.add_command(label='バージョン情報', underline=8, command=self.menuHelpVersion)
    root['menu'] = menu

  def menuFileNew(self):
    self._encoding = self._defaultEncoding
    self.textFilename = ''
    self.text.delete('1.0', 'end')

  def menuFileOpen(self):
    filename = filedialog.askopenfilename(filetypes=self.fileTypes, initialdir=self.directory)
    if not filename:
      return
    
    newText = ''
    try:
      f = open(filename, 'r')
      newText = f.read()
      self._encoding = 'SHIFT_JIS'
    except:
      f = open(filename, 'r', encoding='UTF-8')
      newText = f.read()
      self._encoding = 'UTF-8'
    finally: 
      f.close()

    if newText == '':
      messagebox.showwarning(self.__class__.__name__, 'ファイルを開けませんでした')
    else:
      self.text.delete('1.0', 'end')
      self.text.insert('1.0', newText)
      self.textFilename = filename

  def menuFileSave(self):
    self.fileSave(self.textFilename)

  def fileSave(self, saveFilename):
    s = self.text.get('1.0', 'end')

    if len(s) == 1:
      messagebox.showwarning(self.__class__.__name__, '保存するテキストがありません')
      return

    f = open(saveFilename, 'w', encoding=self._encoding)
    f.write(s[:-1])
    f.close()
    self.textFilename = saveFilename

  def fileSaveAs(self):
    filename = filedialog.asksaveasfilename(filetypes=self.fileTypes, initialdir=self.directory, initialfile=os.path.basename(self.textFilename))
    if not filename:
      return
    self.fileSave(filename)

  def menuFileExit(self):
    cp = configparser.ConfigParser()
    cp['Client'] = {
      'Height': str(root.winfo_height()),
      'Width': str(root.winfo_width())}
    cp['File'] = {'Directory': self.directory}

    with open(self.__class__.__name__ + '.ini', 'w') as f:
      cp.write(f)
    root.destroy()

  def menuHelpOpenReleaseNotes(self):
    webbrowser.open('https://github.com/webcyou-org/text-editor-awesome')

  def menuHelpVersion(self):
    s = self.__class__.__name__ + '\n\n'
    s += 'バージョン: 0.1.0\n'
    s += 'コミット: \n'
    s += '日付: \n'
    s += 'with Python: ' + sys.version
    messagebox.showinfo(self.__class__.__name__, s)

root = Tk()
TextEdit(root)
root.mainloop()