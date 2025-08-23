import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTabWidget, QTextEdit,
                             QFileDialog, QSizePolicy, QMenu, QMessageBox, QLabel)
from PyQt6.QtGui import QIcon, QTextCharFormat, QTextCursor, QFont, QPixmap
from PyQt6.QtCore import Qt, QSize, QDir

class ScribbleApp(QMainWindow):
    """
    Scribble is a simple notepad application with a custom UI
    and basic text formatting features.
    """
    def __init__(self):
        """Initializes the main application window and its components."""
        super().__init__()

        self.setWindowTitle("Scribble")
        self.setGeometry(100, 100, 800, 600)

        # Set the main window's style to match the requested UI
        self.setStyleSheet("""
            QMainWindow {
                background-color: #363636;
                border: 2px solid #5a5a5a;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton {
                background-color: #5a5a5a;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 15px;
                font-family: sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
            QTextEdit {
                background-color: #4a4a4a;
                color: white;
                border: 2px solid #5a5a5a;
                border-radius: 15px;
                padding: 15px;
                font-family: sans-serif;
                font-size: 14px;
            }
            QTabWidget::pane {
                border: none;
                background-color: #363636;
                padding-top: 15px;
            }
            QTabWidget > QWidget {
                background-color: #4a4a4a;
                border-radius: 15px;
            }
            QTabBar::tab {
                background: #5a5a5a;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 15px;
                margin: 5px;
            }
            QTabBar::tab:selected {
                background: #4a4a4a;
            }
            QTabBar::tab:!selected {
                background: #5a5a5a;
            }
            QTabBar::tab:hover {
                background-color: #6a6a6a;
            }
            QTabBar::close-button {
                image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" viewBox="0 0 16 16"><path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/></svg>);
                subcontrol-position: right;
                background-color: #ff5555;
                border-radius: 8px;
                width: 16px;
                height: 16px;
                margin-left: 5px;
            }
            QTabBar::close-button:hover {
                background-color: #ff3333;
            }
            QMenu {
                background-color: #5a5a5a;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item:selected {
                background-color: #6a6a6a;
            }
            #closeBtn {
                background-color: #ff5555;
            }
            #closeBtn:hover {
                background-color: #ff3333;
            }
            #maximizeBtn, #minimizeBtn {
                background-color: #5a5a5a;
            }
            #maximizeBtn:hover, #minimizeBtn:hover {
                background-color: #6a6a6a;
            }
            #appTitleLabel {
                background-color: #4a4a4a;
                font-size: 16px;
                font-weight: bold;
                color: white;
                border-radius: 15px;
                padding: 5px 10px;
                min-width: 120px;
                text-align: center;
            }
            QTextEdit::placeholder {
                color: #b6b6b6;
            }
            QPushButton#strikethroughBtn {
                text-decoration: line-through;
            }
        """)

        # Set window flags to create a frameless window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        # Create top bar layout for the title, formatting buttons, and file menu
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        # App Logo (now an image)
        app_logo = QLabel()
        app_logo.setObjectName("appTitleLabel")
        pixmap = QPixmap("logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(QSize(120, 40), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            app_logo.setPixmap(scaled_pixmap)
        else:
            app_logo.setText("Scribble")
            app_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            print("Warning: Could not load logo.png. Displaying 'Scribble' text instead.")

        # New Tab button (+)
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setFixedSize(QSize(40, 40))
        self.new_tab_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                font-size: 20px;
                color: white;
                border-radius: 15px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
        """)
        self.new_tab_btn.clicked.connect(self.new_document)
        
        # Spacing to push buttons to the center
        top_bar_layout.addWidget(app_logo)
        top_bar_layout.addWidget(self.new_tab_btn)
        top_bar_layout.addStretch()

        # Formatting buttons
        self.bold_btn = QPushButton("B")
        self.bold_btn.setCheckable(True)
        self.bold_btn.setFixedSize(QSize(40, 40))
        self.bold_btn.clicked.connect(self.toggle_bold)

        self.underline_btn = QPushButton("U")
        self.underline_btn.setCheckable(True)
        self.underline_btn.setFixedSize(QSize(40, 40))
        self.underline_btn.clicked.connect(self.toggle_underline)

        self.strikethrough_btn = QPushButton("S")
        self.strikethrough_btn.setObjectName("strikethroughBtn")
        self.strikethrough_btn.setCheckable(True)
        self.strikethrough_btn.setFixedSize(QSize(40, 40))
        self.strikethrough_btn.clicked.connect(self.toggle_strikethrough)

        self.italic_btn = QPushButton("I")
        self.italic_btn.setCheckable(True)
        self.italic_btn.setFixedSize(QSize(40, 40))
        self.italic_btn.clicked.connect(self.toggle_italic)
        
        # New text size button and menu
        self.text_size_btn = QPushButton("Size")
        self.text_size_btn.setFixedSize(QSize(120, 40))
        self.text_size_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                font-size: 14px;
                color: white;
                border-radius: 15px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
        """)
        
        text_size_menu = QMenu(self)
        for size in [10, 12, 14, 16, 18, 20]:
            action = text_size_menu.addAction(str(size))
            action.triggered.connect(lambda checked, s=size: self.set_font_size(s))
        self.text_size_btn.setMenu(text_size_menu)

        # Style the formatting buttons
        formatting_buttons_style = """
            QPushButton {
                background-color: #4a4a4a;
                border-radius: 15px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
            QPushButton:checked {
                background-color: #3b3b3b;
                border: 2px solid #b6b6b6;
            }
        """
        self.bold_btn.setStyleSheet(formatting_buttons_style)
        self.underline_btn.setStyleSheet(formatting_buttons_style)
        self.strikethrough_btn.setStyleSheet(formatting_buttons_style)
        self.italic_btn.setStyleSheet(formatting_buttons_style)

        # File Menu button
        self.file_menu_btn = QPushButton("File ↓")
        self.file_menu_btn.setFixedSize(QSize(80, 40))
        self.file_menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                font-size: 14px;
                color: white;
                border-radius: 15px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
        """)

        # Create the file menu
        file_menu = QMenu(self)
        file_menu.addAction("New", self.new_document)
        file_menu.addAction("Open...", self.open_file)
        file_menu.addAction("Save", self.save_file)
        file_menu.addAction("Save As...", self.save_as_file)
        file_menu.addSeparator()
        file_menu.addAction("About", self.open_about_page)
        file_menu.addAction("Exit", self.close)
        
        self.file_menu_btn.setMenu(file_menu)

        # Add buttons to the layout
        top_bar_layout.addWidget(self.bold_btn)
        top_bar_layout.addWidget(self.underline_btn)
        top_bar_layout.addWidget(self.strikethrough_btn)
        top_bar_layout.addWidget(self.italic_btn)
        top_bar_layout.addWidget(self.text_size_btn)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.file_menu_btn)
        
        # Window control buttons layout
        window_control_layout = QHBoxLayout()
        window_control_layout.setSpacing(5)

        self.minimize_btn = QPushButton("-")
        self.minimize_btn.setObjectName("minimizeBtn")
        self.minimize_btn.setFixedSize(QSize(30, 30))
        self.minimize_btn.clicked.connect(self.showMinimized)

        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setObjectName("maximizeBtn")
        self.maximize_btn.setFixedSize(QSize(30, 30))
        self.maximize_btn.clicked.connect(self.toggle_maximize_restore)

        self.close_btn = QPushButton("X")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(QSize(30, 30))
        self.close_btn.clicked.connect(self.close)

        window_control_layout.addWidget(self.minimize_btn)
        window_control_layout.addWidget(self.maximize_btn)
        window_control_layout.addWidget(self.close_btn)

        top_bar_layout.addLayout(window_control_layout)
        self.main_layout.addLayout(top_bar_layout)
        
        # Tab widget for multiple documents
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_format_buttons)
        self.main_layout.addWidget(self.tab_widget)
        
        # Initial empty document
        self.new_document()
        
    def toggle_maximize_restore(self):
        """Toggles between maximized and normal window state."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def new_document(self):
        """Creates a new, empty document tab."""
        text_edit = QTextEdit()
        text_edit.setPlaceholderText("Type here...")
        text_edit.setAcceptRichText(True)
        text_edit.textChanged.connect(self.document_modified)
        text_edit.cursorPositionChanged.connect(self.update_format_buttons)
        
        tab_count = self.tab_widget.count() + 1
        self.tab_widget.addTab(text_edit, f"Untitled-{tab_count}")
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
        text_edit.setFocus()
        
    def document_modified(self):
        """Marks the current document as modified."""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            tab_text = self.tab_widget.tabText(current_index)
            if not tab_text.endswith("*"):
                self.tab_widget.setTabText(current_index, tab_text + "*")
        
    def close_tab(self, index):
        """Handles closing a tab, with a save prompt if needed."""
        text_edit = self.tab_widget.widget(index)
        tab_text = self.tab_widget.tabText(index)
        
        if tab_text.endswith("*"):
            reply = QMessageBox.warning(self, "Unsaved Changes",
                                        "You have unsaved changes. Do you want to save?",
                                        QMessageBox.StandardButton.Save |
                                        QMessageBox.StandardButton.Discard |
                                        QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
                self.tab_widget.removeTab(index)
                text_edit.deleteLater()
            elif reply == QMessageBox.StandardButton.Discard:
                self.tab_widget.removeTab(index)
                text_edit.deleteLater() # FIX: Added this line to properly delete the widget
            # If Cancel, do nothing
        else:
            self.tab_widget.removeTab(index)
            text_edit.deleteLater()
        
    def open_file(self):
        """Opens a file and loads its content into a new tab."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "HTML Files (*.html);;Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                # Determine if the file is HTML or plain text based on extension
                if file_path.lower().endswith('.html'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        text_edit = QTextEdit()
                        text_edit.setHtml(content) # Load as HTML to keep formatting
                else: # Fallback to plain text for .txt and other file types
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        text_edit = QTextEdit()
                        text_edit.setPlainText(content)
                        
                text_edit.textChanged.connect(self.document_modified)
                text_edit.cursorPositionChanged.connect(self.update_format_buttons)

                file_name = QDir(file_path).dirName()
                self.tab_widget.addTab(text_edit, file_name)
                self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
                text_edit.setFocus()
            except Exception as e:
                print(f"Error opening file: {e}")
                
    def save_file(self):
        """Saves the current file to its path, or calls save_as_file if it's new."""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            text_edit = self.tab_widget.currentWidget()
            tab_text = self.tab_widget.tabText(current_index)
            
            if tab_text.startswith("Untitled-"):
                self.save_as_file()
            else:
                file_path = tab_text.rstrip('*')
                try:
                    # Save based on file extension to preserve formatting if it's an HTML file
                    if file_path.lower().endswith('.html'):
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(text_edit.toHtml())
                    else: # For other files, save as plain text
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(text_edit.toPlainText())
                            
                    self.tab_widget.setTabText(current_index, tab_text.rstrip('*'))
                except Exception as e:
                    print(f"Error saving file: {e}")
                    
    def save_as_file(self):
        """Prompts the user to select a path and saves the current file."""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            text_edit = self.tab_widget.currentWidget()
            file_path, selected_filter = QFileDialog.getSaveFileName(self, "Save File As", "", "HTML Files (*.html);;Text Files (*.txt);;All Files (*)")
            if file_path:
                try:
                    # Save as HTML or plain text based on the selected filter
                    if selected_filter.endswith('.html)'):
                        content_to_save = text_edit.toHtml()
                    else:
                        content_to_save = text_edit.toPlainText()
                        if selected_filter.endswith('.txt)'):
                            QMessageBox.information(self, "Plain Text Save", "Note: Saving as plain text will remove all rich text formatting like bold and italics.")

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content_to_save)

                    file_name = QDir(file_path).dirName()
                    self.tab_widget.setTabText(current_index, file_name)
                except Exception as e:
                    print(f"Error saving file: {e}")
                
    def toggle_bold(self):
        """Toggles bold formatting for the selected text."""
        text_edit = self.tab_widget.currentWidget()
        if text_edit:
            cursor = text_edit.textCursor()
            if not cursor.hasSelection():
                cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            
            char_format = cursor.charFormat()
            weight = QFont.Weight.Bold if char_format.fontWeight() == QFont.Weight.Normal else QFont.Weight.Normal
            char_format.setFontWeight(weight)
            cursor.mergeCharFormat(char_format)
            self.update_format_buttons()
            
    def toggle_underline(self):
        """Toggles underline formatting for the selected text."""
        text_edit = self.tab_widget.currentWidget()
        if text_edit:
            cursor = text_edit.textCursor()
            if not cursor.hasSelection():
                cursor.select(QTextCursor.SelectionType.WordUnderCursor)
                
            char_format = cursor.charFormat()
            char_format.setFontUnderline(not char_format.fontUnderline())
            cursor.mergeCharFormat(char_format)
            self.update_format_buttons()
            
    def toggle_strikethrough(self):
        """Toggles strikethrough formatting for the selected text."""
        text_edit = self.tab_widget.currentWidget()
        if text_edit:
            cursor = text_edit.textCursor()
            if not cursor.hasSelection():
                cursor.select(QTextCursor.SelectionType.WordUnderCursor)
                
            char_format = cursor.charFormat()
            char_format.setFontStrikeOut(not char_format.fontStrikeOut())
            cursor.mergeCharFormat(char_format)
            self.update_format_buttons()

    def toggle_italic(self):
        """Toggles italic formatting for the selected text."""
        text_edit = self.tab_widget.currentWidget()
        if text_edit:
            cursor = text_edit.textCursor()
            if not cursor.hasSelection():
                cursor.select(QTextCursor.SelectionType.WordUnderCursor)
                
            char_format = cursor.charFormat()
            char_format.setFontItalic(not char_format.fontItalic())
            cursor.mergeCharFormat(char_format)
            self.update_format_buttons()
            
    def set_font_size(self, size):
        """Sets the font size of the selected text."""
        text_edit = self.tab_widget.currentWidget()
        if text_edit:
            cursor = text_edit.textCursor()
            char_format = cursor.charFormat()
            char_format.setFontPointSize(size)
            cursor.mergeCharFormat(char_format)
            self.update_format_buttons()

    def update_format_buttons(self):
        """
        Updates the checked state of formatting buttons based on the
        current cursor's character format.
        """
        text_edit = self.tab_widget.currentWidget()
        if text_edit:
            char_format = text_edit.textCursor().charFormat()
            
            self.bold_btn.setChecked(char_format.fontWeight() == QFont.Weight.Bold)
            self.underline_btn.setChecked(char_format.fontUnderline())
            self.strikethrough_btn.setChecked(char_format.fontStrikeOut())
            self.italic_btn.setChecked(char_format.fontItalic())
            self.text_size_btn.setText(f"Size: {int(char_format.fontPointSize())}")
        else:
            self.bold_btn.setChecked(False)
            self.underline_btn.setChecked(False)
            self.strikethrough_btn.setChecked(False)
            self.italic_btn.setChecked(False)
            self.text_size_btn.setText("Size")

    def open_about_page(self):
        """Opens a new tab with a predefined about page."""
        # HTML content for the about page
        about_html = """
        <html>
        <body style="background-color: #4a4a4a; color: white; font-family: sans-serif; padding: 20px;">
            <h1 style="color: #ffffff; text-align: center;">About Scribble</h1>
            <p style="font-size: 16px; line-height: 1.6;">
            
            (Scribble Version: v1.6)   
            (Python Version: 3.11)     
            
                Scribble is a simple yet good-looking notepad application built with Python.     
                
                 Made By Whale64!
                

            <hr style="border: 1px solid #6a6a6a;">
            <p style="font-size: 14px; text-align: right;">
                Version 1.0.0
            </p>
        </body>
        </html>
        """
        
        # Create a new QTextEdit for the about page
        about_text_edit = QTextEdit()
        about_text_edit.setHtml(about_html)
        about_text_edit.setReadOnly(True) # Make it read-only
        
        # Add the new tab
        self.tab_widget.addTab(about_text_edit, "About Scribble")
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScribbleApp()
    window.show()
    sys.exit(app.exec())
