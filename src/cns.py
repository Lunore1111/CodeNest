from PySide6.QtWidgets import QApplication , QMainWindow , QVBoxLayout ,QWidget
from PySide6.QtWidgets import QPlainTextEdit , QPushButton , QLabel
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt, QSize


class open_file(QWidget):
    file_loaded = Signal(str) # this signal will carry file data str is data we have to pass
    file_name = Signal(str) 
    def __init__(self,stack_panels):
        super().__init__()
        self.stack_panels = stack_panels
        self.file_content =""
        self.label_for_open = QLabel("Open file")
        self.open_button = QPushButton("Open")
        self.open_file_layout = QVBoxLayout()
        self.open_file_layout.addWidget(self.label_for_open)
        self.open_file_layout.addWidget(self.open_button)
        self.setLayout(self.open_file_layout)
        self.open_file_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.open_button.clicked.connect(self.open_file_dialog)
        
    def open_file_dialog(self):    
        file_path,_ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "", # starting dict
            "All Files (*)"  # file filter
        )
        if file_path:
            with open(file_path,"r") as file_read:
                self.file_content = file_read.read()
                self.stack_panels.setCurrentIndex(1)
                self.file_loaded.emit(self.file_content) # passing self.file_content as data /str 
                self.get_file_name = file_path
                self.file_name.emit(self.get_file_name)
        else:
            QMessageBox(
                self,
                "Error"
                "Pls select any file to open !!!"
            )

class editor_part(QMainWindow):
    def __init__(self,open_file,stack_panels):
        super().__init__()
        self.stackpanels = stack_panels
        self.open_file = open_file
        self.widget = QWidget()
        self.widget.layout_box = QVBoxLayout()
        self.widget.editor = QPlainTextEdit()
        self.widget.save = QPushButton("Save")
        self.widget.back = QPushButton("Go Back")
        self.widget.layout_box.addWidget(self.widget.editor)
        self.widget.layout_box.addWidget(self.widget.save)
        self.widget.layout_box.addWidget(self.widget.back)
        self.widget.setLayout(self.widget.layout_box)
        self.widget.layout_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.widget)
        self.widget.save.clicked.connect(self.save_to_file)
        self.open_file.file_loaded.connect(self.update_buffer)
        self.widget.back.clicked.connect(self.go_back)
    def save_to_file(self):
        strings = self.widget.editor.toPlainText()
        with open(self.open_file.get_file_name,"w") as write_file:
            write_file.write(strings)
    def update_buffer(self):
        self.widget.editor.setPlainText(self.open_file.file_content)
    def go_back(self):
        self.stackpanels.setCurrentIndex(0)
        
app = QApplication([])

stack_panels = QStackedWidget()

select_file_page = open_file(stack_panels)
editor = editor_part(select_file_page,stack_panels)

stack_panels.addWidget(select_file_page) # 0 
stack_panels.addWidget(editor) #1
stack_panels.show() 
 
app.exec()