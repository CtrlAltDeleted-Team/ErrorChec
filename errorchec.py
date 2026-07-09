import sys
import os
import re
import random
import time
import subprocess
import tempfile
import shutil
import platform
import json
import urllib.request
import zipfile
import threading
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QListWidget, QListWidgetItem, QMenuBar, QMenu,
    QFileDialog, QMessageBox, QDialog, QDialogButtonBox, QComboBox,
    QPushButton, QLabel, QSplitter, QCheckBox, QSpinBox, QTabWidget,
    QInputDialog, QLineEdit, QProgressDialog, QGroupBox, QGridLayout,
    QScrollArea, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRegularExpression, QThread
from PyQt6.QtGui import QFont, QAction, QTextCursor, QColor, QTextCharFormat, QSyntaxHighlighter, QFontDatabase, QIcon, QPainter, QBrush

from multiprocessing import freeze_support

THEMES = {
    'dark_01': {
        'bg_color': '#1e1e1e', 'text_color': '#ffffff', 'editor_bg': '#2d2d2d',
        'editor_text': '#ffffff', 'border_color': '#3d3d3d', 'list_bg': '#2d2d2d',
        'list_text': '#ffffff', 'menu_bg': '#1e1e1e', 'menu_text': '#ffffff',
        'menu_hover': '#2d2d2d', 'button_bg': '#3498db', 'button_text': '#ffffff',
        'button_hover': '#2980b9', 'progress_bg': '#2d2d2d', 'progress_chunk': '#3498db',
        'scroll_bg': '#2d2d2d', 'scroll_handle': '#555555', 'scroll_handle_hover': '#666666'
    },
    'dark_02': {
        'bg_color': '#0a0a0a', 'text_color': '#ffffff', 'editor_bg': '#1a1a1a',
        'editor_text': '#f0f0f0', 'border_color': '#333333', 'list_bg': '#1a1a1a',
        'list_text': '#f0f0f0', 'menu_bg': '#0a0a0a', 'menu_text': '#ffffff',
        'menu_hover': '#2a2a2a', 'button_bg': '#e74c3c', 'button_text': '#ffffff',
        'button_hover': '#c0392b', 'progress_bg': '#1a1a1a', 'progress_chunk': '#e74c3c',
        'scroll_bg': '#1a1a1a', 'scroll_handle': '#444444', 'scroll_handle_hover': '#555555'
    },
    'dark_03': {
        'bg_color': '#1a1a2e', 'text_color': '#ffffff', 'editor_bg': '#16213e',
        'editor_text': '#e0e0e0', 'border_color': '#0f3460', 'list_bg': '#16213e',
        'list_text': '#e0e0e0', 'menu_bg': '#1a1a2e', 'menu_text': '#ffffff',
        'menu_hover': '#16213e', 'button_bg': '#e94560', 'button_text': '#ffffff',
        'button_hover': '#c73652', 'progress_bg': '#16213e', 'progress_chunk': '#e94560',
        'scroll_bg': '#16213e', 'scroll_handle': '#0f3460', 'scroll_handle_hover': '#1a4a80'
    },
    'dark_04': {
        'bg_color': '#2b2b2b', 'text_color': '#a9b7c6', 'editor_bg': '#313335',
        'editor_text': '#a9b7c6', 'border_color': '#464646', 'list_bg': '#313335',
        'list_text': '#a9b7c6', 'menu_bg': '#2b2b2b', 'menu_text': '#a9b7c6',
        'menu_hover': '#313335', 'button_bg': '#6897bb', 'button_text': '#ffffff',
        'button_hover': '#4f7a99', 'progress_bg': '#313335', 'progress_chunk': '#6897bb',
        'scroll_bg': '#313335', 'scroll_handle': '#464646', 'scroll_handle_hover': '#555555'
    },
    'dark_05': {
        'bg_color': '#282c34', 'text_color': '#abb2bf', 'editor_bg': '#21252b',
        'editor_text': '#abb2bf', 'border_color': '#3e4451', 'list_bg': '#21252b',
        'list_text': '#abb2bf', 'menu_bg': '#282c34', 'menu_text': '#abb2bf',
        'menu_hover': '#21252b', 'button_bg': '#61afef', 'button_text': '#ffffff',
        'button_hover': '#4a9ad9', 'progress_bg': '#21252b', 'progress_chunk': '#61afef',
        'scroll_bg': '#21252b', 'scroll_handle': '#3e4451', 'scroll_handle_hover': '#4a5568'
    },
    'dark_06': {
        'bg_color': '#1d1f21', 'text_color': '#c5c8c6', 'editor_bg': '#1d1f21',
        'editor_text': '#c5c8c6', 'border_color': '#373b41', 'list_bg': '#1d1f21',
        'list_text': '#c5c8c6', 'menu_bg': '#1d1f21', 'menu_text': '#c5c8c6',
        'menu_hover': '#282a2e', 'button_bg': '#81a2be', 'button_text': '#ffffff',
        'button_hover': '#668aa3', 'progress_bg': '#1d1f21', 'progress_chunk': '#81a2be',
        'scroll_bg': '#1d1f21', 'scroll_handle': '#373b41', 'scroll_handle_hover': '#4d535e'
    },
    'dark_07': {
        'bg_color': '#1e1e2f', 'text_color': '#cdd6f4', 'editor_bg': '#181825',
        'editor_text': '#cdd6f4', 'border_color': '#313244', 'list_bg': '#181825',
        'list_text': '#cdd6f4', 'menu_bg': '#1e1e2f', 'menu_text': '#cdd6f4',
        'menu_hover': '#181825', 'button_bg': '#89b4fa', 'button_text': '#1e1e2f',
        'button_hover': '#74c7ec', 'progress_bg': '#181825', 'progress_chunk': '#89b4fa',
        'scroll_bg': '#181825', 'scroll_handle': '#313244', 'scroll_handle_hover': '#45475a'
    },
    'dark_08': {
        'bg_color': '#0d1117', 'text_color': '#c9d1d9', 'editor_bg': '#161b22',
        'editor_text': '#c9d1d9', 'border_color': '#30363d', 'list_bg': '#161b22',
        'list_text': '#c9d1d9', 'menu_bg': '#0d1117', 'menu_text': '#c9d1d9',
        'menu_hover': '#161b22', 'button_bg': '#238636', 'button_text': '#ffffff',
        'button_hover': '#2ea043', 'progress_bg': '#161b22', 'progress_chunk': '#238636',
        'scroll_bg': '#161b22', 'scroll_handle': '#30363d', 'scroll_handle_hover': '#484f58'
    },
    'dark_09': {
        'bg_color': '#1a1b26', 'text_color': '#a9b1d6', 'editor_bg': '#24283b',
        'editor_text': '#a9b1d6', 'border_color': '#414868', 'list_bg': '#24283b',
        'list_text': '#a9b1d6', 'menu_bg': '#1a1b26', 'menu_text': '#a9b1d6',
        'menu_hover': '#24283b', 'button_bg': '#7aa2f7', 'button_text': '#1a1b26',
        'button_hover': '#89b4fa', 'progress_bg': '#24283b', 'progress_chunk': '#7aa2f7',
        'scroll_bg': '#24283b', 'scroll_handle': '#414868', 'scroll_handle_hover': '#565f89'
    },
    'dark_10': {
        'bg_color': '#2c2c2c', 'text_color': '#d4d4d4', 'editor_bg': '#1e1e1e',
        'editor_text': '#d4d4d4', 'border_color': '#3c3c3c', 'list_bg': '#1e1e1e',
        'list_text': '#d4d4d4', 'menu_bg': '#2c2c2c', 'menu_text': '#d4d4d4',
        'menu_hover': '#1e1e1e', 'button_bg': '#569cd6', 'button_text': '#ffffff',
        'button_hover': '#4a8ab5', 'progress_bg': '#1e1e1e', 'progress_chunk': '#569cd6',
        'scroll_bg': '#1e1e1e', 'scroll_handle': '#3c3c3c', 'scroll_handle_hover': '#4c4c4c'
    },
    'dark_11': {
        'bg_color': '#1a1a1a', 'text_color': '#e0e0e0', 'editor_bg': '#252525',
        'editor_text': '#e0e0e0', 'border_color': '#404040', 'list_bg': '#252525',
        'list_text': '#e0e0e0', 'menu_bg': '#1a1a1a', 'menu_text': '#e0e0e0',
        'menu_hover': '#252525', 'button_bg': '#ff6b6b', 'button_text': '#ffffff',
        'button_hover': '#ee5a24', 'progress_bg': '#252525', 'progress_chunk': '#ff6b6b',
        'scroll_bg': '#252525', 'scroll_handle': '#404040', 'scroll_handle_hover': '#555555'
    },
    'dark_12': {
        'bg_color': '#0c0c0c', 'text_color': '#00ff00', 'editor_bg': '#0a0a0a',
        'editor_text': '#00ff00', 'border_color': '#00aa00', 'list_bg': '#0a0a0a',
        'list_text': '#00ff00', 'menu_bg': '#0c0c0c', 'menu_text': '#00ff00',
        'menu_hover': '#0a0a0a', 'button_bg': '#00ff00', 'button_text': '#000000',
        'button_hover': '#00cc00', 'progress_bg': '#0a0a0a', 'progress_chunk': '#00ff00',
        'scroll_bg': '#0a0a0a', 'scroll_handle': '#00aa00', 'scroll_handle_hover': '#00cc00'
    },
    'dark_13': {
        'bg_color': '#1b0a1e', 'text_color': '#e0b0ff', 'editor_bg': '#2d1333',
        'editor_text': '#e0b0ff', 'border_color': '#4a1a5a', 'list_bg': '#2d1333',
        'list_text': '#e0b0ff', 'menu_bg': '#1b0a1e', 'menu_text': '#e0b0ff',
        'menu_hover': '#2d1333', 'button_bg': '#9b59b6', 'button_text': '#ffffff',
        'button_hover': '#8e44ad', 'progress_bg': '#2d1333', 'progress_chunk': '#9b59b6',
        'scroll_bg': '#2d1333', 'scroll_handle': '#4a1a5a', 'scroll_handle_hover': '#5a2a6a'
    },
    'dark_14': {
        'bg_color': '#002b36', 'text_color': '#839496', 'editor_bg': '#073642',
        'editor_text': '#839496', 'border_color': '#094f5c', 'list_bg': '#073642',
        'list_text': '#839496', 'menu_bg': '#002b36', 'menu_text': '#839496',
        'menu_hover': '#073642', 'button_bg': '#268bd2', 'button_text': '#ffffff',
        'button_hover': '#2aa198', 'progress_bg': '#073642', 'progress_chunk': '#268bd2',
        'scroll_bg': '#073642', 'scroll_handle': '#094f5c', 'scroll_handle_hover': '#0a6b7a'
    },
    'dark_15': {
        'bg_color': '#0f0f1a', 'text_color': '#c0c0d0', 'editor_bg': '#1a1a2e',
        'editor_text': '#c0c0d0', 'border_color': '#2a2a4a', 'list_bg': '#1a1a2e',
        'list_text': '#c0c0d0', 'menu_bg': '#0f0f1a', 'menu_text': '#c0c0d0',
        'menu_hover': '#1a1a2e', 'button_bg': '#4a6fa5', 'button_text': '#ffffff',
        'button_hover': '#3a5a8a', 'progress_bg': '#1a1a2e', 'progress_chunk': '#4a6fa5',
        'scroll_bg': '#1a1a2e', 'scroll_handle': '#2a2a4a', 'scroll_handle_hover': '#3a3a5a'
    },
    
    # Светлые темы
    'light_01': {
        'bg_color': '#f5f5f5', 'text_color': '#333333', 'editor_bg': '#ffffff',
        'editor_text': '#333333', 'border_color': '#ddd', 'list_bg': '#ffffff',
        'list_text': '#333333', 'menu_bg': '#f5f5f5', 'menu_text': '#333333',
        'menu_hover': '#e0e0e0', 'button_bg': '#3498db', 'button_text': '#ffffff',
        'button_hover': '#2980b9', 'progress_bg': '#e0e0e0', 'progress_chunk': '#3498db',
        'scroll_bg': '#e0e0e0', 'scroll_handle': '#cccccc', 'scroll_handle_hover': '#bbbbbb'
    },
    'light_pink': {
        'bg_color': '#fce4ec', 'text_color': '#4a2c2c', 'editor_bg': '#fff5f7',
        'editor_text': '#4a2c2c', 'border_color': '#f8bbd0', 'list_bg': '#fff5f7',
        'list_text': '#4a2c2c', 'menu_bg': '#fce4ec', 'menu_text': '#4a2c2c',
        'menu_hover': '#f8bbd0', 'button_bg': '#e91e63', 'button_text': '#ffffff',
        'button_hover': '#c2185b', 'progress_bg': '#f8bbd0', 'progress_chunk': '#e91e63',
        'scroll_bg': '#f8bbd0', 'scroll_handle': '#f48fb1', 'scroll_handle_hover': '#f06292'
    },
    'light_blue': {
        'bg_color': '#e3f2fd', 'text_color': '#1a237e', 'editor_bg': '#f5faff',
        'editor_text': '#1a237e', 'border_color': '#90caf9', 'list_bg': '#f5faff',
        'list_text': '#1a237e', 'menu_bg': '#e3f2fd', 'menu_text': '#1a237e',
        'menu_hover': '#90caf9', 'button_bg': '#1976d2', 'button_text': '#ffffff',
        'button_hover': '#1565c0', 'progress_bg': '#90caf9', 'progress_chunk': '#1976d2',
        'scroll_bg': '#90caf9', 'scroll_handle': '#64b5f6', 'scroll_handle_hover': '#42a5f5'
    },
    'light_green': {
        'bg_color': '#e8f5e9', 'text_color': '#1b3a1b', 'editor_bg': '#f5fff5',
        'editor_text': '#1b3a1b', 'border_color': '#a5d6a7', 'list_bg': '#f5fff5',
        'list_text': '#1b3a1b', 'menu_bg': '#e8f5e9', 'menu_text': '#1b3a1b',
        'menu_hover': '#a5d6a7', 'button_bg': '#2e7d32', 'button_text': '#ffffff',
        'button_hover': '#1b5e20', 'progress_bg': '#a5d6a7', 'progress_chunk': '#2e7d32',
        'scroll_bg': '#a5d6a7', 'scroll_handle': '#81c784', 'scroll_handle_hover': '#66bb6a'
    },
    'light_purple': {
        'bg_color': '#f3e5f5', 'text_color': '#311b92', 'editor_bg': '#faf5ff',
        'editor_text': '#311b92', 'border_color': '#ce93d8', 'list_bg': '#faf5ff',
        'list_text': '#311b92', 'menu_bg': '#f3e5f5', 'menu_text': '#311b92',
        'menu_hover': '#ce93d8', 'button_bg': '#7b1fa2', 'button_text': '#ffffff',
        'button_hover': '#6a1b9a', 'progress_bg': '#ce93d8', 'progress_chunk': '#7b1fa2',
        'scroll_bg': '#ce93d8', 'scroll_handle': '#ab47bc', 'scroll_handle_hover': '#9c27b0'
    },
    'light_orange': {
        'bg_color': '#fff3e0', 'text_color': '#4e2e0a', 'editor_bg': '#fffaf5',
        'editor_text': '#4e2e0a', 'border_color': '#ffcc80', 'list_bg': '#fffaf5',
        'list_text': '#4e2e0a', 'menu_bg': '#fff3e0', 'menu_text': '#4e2e0a',
        'menu_hover': '#ffcc80', 'button_bg': '#e65100', 'button_text': '#ffffff',
        'button_hover': '#bf360c', 'progress_bg': '#ffcc80', 'progress_chunk': '#e65100',
        'scroll_bg': '#ffcc80', 'scroll_handle': '#ffa726', 'scroll_handle_hover': '#ff9800'
    },
    'light_teal': {
        'bg_color': '#e0f7fa', 'text_color': '#004d40', 'editor_bg': '#f5ffff',
        'editor_text': '#004d40', 'border_color': '#80deea', 'list_bg': '#f5ffff',
        'list_text': '#004d40', 'menu_bg': '#e0f7fa', 'menu_text': '#004d40',
        'menu_hover': '#80deea', 'button_bg': '#00897b', 'button_text': '#ffffff',
        'button_hover': '#00695c', 'progress_bg': '#80deea', 'progress_chunk': '#00897b',
        'scroll_bg': '#80deea', 'scroll_handle': '#4dd0e1', 'scroll_handle_hover': '#26c6da'
    },
    'light_amber': {
        'bg_color': '#fff8e1', 'text_color': '#4e342e', 'editor_bg': '#fffff5',
        'editor_text': '#4e342e', 'border_color': '#ffe082', 'list_bg': '#fffff5',
        'list_text': '#4e342e', 'menu_bg': '#fff8e1', 'menu_text': '#4e342e',
        'menu_hover': '#ffe082', 'button_bg': '#f57f17', 'button_text': '#ffffff',
        'button_hover': '#e65100', 'progress_bg': '#ffe082', 'progress_chunk': '#f57f17',
        'scroll_bg': '#ffe082', 'scroll_handle': '#ffb300', 'scroll_handle_hover': '#ffa000'
    },
    'light_cyan': {
        'bg_color': '#e0f7fa', 'text_color': '#006064', 'editor_bg': '#f5ffff',
        'editor_text': '#006064', 'border_color': '#80deea', 'list_bg': '#f5ffff',
        'list_text': '#006064', 'menu_bg': '#e0f7fa', 'menu_text': '#006064',
        'menu_hover': '#80deea', 'button_bg': '#00acc1', 'button_text': '#ffffff',
        'button_hover': '#00838f', 'progress_bg': '#80deea', 'progress_chunk': '#00acc1',
        'scroll_bg': '#80deea', 'scroll_handle': '#26c6da', 'scroll_handle_hover': '#00bcd4'
    },
    'light_lime': {
        'bg_color': '#f0f4c3', 'text_color': '#33691e', 'editor_bg': '#fafff5',
        'editor_text': '#33691e', 'border_color': '#c5e1a5', 'list_bg': '#fafff5',
        'list_text': '#33691e', 'menu_bg': '#f0f4c3', 'menu_text': '#33691e',
        'menu_hover': '#c5e1a5', 'button_bg': '#689f38', 'button_text': '#ffffff',
        'button_hover': '#558b2f', 'progress_bg': '#c5e1a5', 'progress_chunk': '#689f38',
        'scroll_bg': '#c5e1a5', 'scroll_handle': '#aed581', 'scroll_handle_hover': '#9ccc65'
    },
    'light_brown': {
        'bg_color': '#efebe9', 'text_color': '#3e2723', 'editor_bg': '#faf5f3',
        'editor_text': '#3e2723', 'border_color': '#bcaaa4', 'list_bg': '#faf5f3',
        'list_text': '#3e2723', 'menu_bg': '#efebe9', 'menu_text': '#3e2723',
        'menu_hover': '#bcaaa4', 'button_bg': '#6d4c41', 'button_text': '#ffffff',
        'button_hover': '#4e342e', 'progress_bg': '#bcaaa4', 'progress_chunk': '#6d4c41',
        'scroll_bg': '#bcaaa4', 'scroll_handle': '#a1887f', 'scroll_handle_hover': '#8d6e63'
    },
    'light_red': {
        'bg_color': '#ffebee', 'text_color': '#4a0a0a', 'editor_bg': '#fff5f5',
        'editor_text': '#4a0a0a', 'border_color': '#ef9a9a', 'list_bg': '#fff5f5',
        'list_text': '#4a0a0a', 'menu_bg': '#ffebee', 'menu_text': '#4a0a0a',
        'menu_hover': '#ef9a9a', 'button_bg': '#c62828', 'button_text': '#ffffff',
        'button_hover': '#b71c1c', 'progress_bg': '#ef9a9a', 'progress_chunk': '#c62828',
        'scroll_bg': '#ef9a9a', 'scroll_handle': '#e57373', 'scroll_handle_hover': '#ef5350'
    },
    'light_deep_purple': {
        'bg_color': '#ede7f6', 'text_color': '#311b92', 'editor_bg': '#f5f0ff',
        'editor_text': '#311b92', 'border_color': '#b39ddb', 'list_bg': '#f5f0ff',
        'list_text': '#311b92', 'menu_bg': '#ede7f6', 'menu_text': '#311b92',
        'menu_hover': '#b39ddb', 'button_bg': '#4527a0', 'button_text': '#ffffff',
        'button_hover': '#311b92', 'progress_bg': '#b39ddb', 'progress_chunk': '#4527a0',
        'scroll_bg': '#b39ddb', 'scroll_handle': '#9575cd', 'scroll_handle_hover': '#7e57c2'
    },
    'light_sky': {
        'bg_color': '#e1f5fe', 'text_color': '#01579b', 'editor_bg': '#f5faff',
        'editor_text': '#01579b', 'border_color': '#81d4fa', 'list_bg': '#f5faff',
        'list_text': '#01579b', 'menu_bg': '#e1f5fe', 'menu_text': '#01579b',
        'menu_hover': '#81d4fa', 'button_bg': '#0277bd', 'button_text': '#ffffff',
        'button_hover': '#01579b', 'progress_bg': '#81d4fa', 'progress_chunk': '#0277bd',
        'scroll_bg': '#81d4fa', 'scroll_handle': '#4fc3f7', 'scroll_handle_hover': '#29b6f6'
    },
    'light_mint': {
        'bg_color': '#e0f2f1', 'text_color': '#004d40', 'editor_bg': '#f5ffff',
        'editor_text': '#004d40', 'border_color': '#80cbc4', 'list_bg': '#f5ffff',
        'list_text': '#004d40', 'menu_bg': '#e0f2f1', 'menu_text': '#004d40',
        'menu_hover': '#80cbc4', 'button_bg': '#00796b', 'button_text': '#ffffff',
        'button_hover': '#00695c', 'progress_bg': '#80cbc4', 'progress_chunk': '#00796b',
        'scroll_bg': '#80cbc4', 'scroll_handle': '#4db6ac', 'scroll_handle_hover': '#26a69a'
    },
    'light_coral': {
        'bg_color': '#fbe9e7', 'text_color': '#4a1a0a', 'editor_bg': '#fff5f2',
        'editor_text': '#4a1a0a', 'border_color': '#ffab91', 'list_bg': '#fff5f2',
        'list_text': '#4a1a0a', 'menu_bg': '#fbe9e7', 'menu_text': '#4a1a0a',
        'menu_hover': '#ffab91', 'button_bg': '#d84315', 'button_text': '#ffffff',
        'button_hover': '#bf360c', 'progress_bg': '#ffab91', 'progress_chunk': '#d84315',
        'scroll_bg': '#ffab91', 'scroll_handle': '#ff8a65', 'scroll_handle_hover': '#ff7043'
    },
    'light_rose': {
        'bg_color': '#fce4ec', 'text_color': '#4a1a2c', 'editor_bg': '#fff5f7',
        'editor_text': '#4a1a2c', 'border_color': '#f48fb1', 'list_bg': '#fff5f7',
        'list_text': '#4a1a2c', 'menu_bg': '#fce4ec', 'menu_text': '#4a1a2c',
        'menu_hover': '#f48fb1', 'button_bg': '#ad1457', 'button_text': '#ffffff',
        'button_hover': '#880e4f', 'progress_bg': '#f48fb1', 'progress_chunk': '#ad1457',
        'scroll_bg': '#f48fb1', 'scroll_handle': '#f06292', 'scroll_handle_hover': '#ec407a'
    },
    'light_cream': {
        'bg_color': '#fff8e1', 'text_color': '#4e342e', 'editor_bg': '#fffff5',
        'editor_text': '#4e342e', 'border_color': '#ffe082', 'list_bg': '#fffff5',
        'list_text': '#4e342e', 'menu_bg': '#fff8e1', 'menu_text': '#4e342e',
        'menu_hover': '#ffe082', 'button_bg': '#f9a825', 'button_text': '#ffffff',
        'button_hover': '#f57f17', 'progress_bg': '#ffe082', 'progress_chunk': '#f9a825',
        'scroll_bg': '#ffe082', 'scroll_handle': '#ffd54f', 'scroll_handle_hover': '#ffca28'
    },
    'light_lavender': {
        'bg_color': '#e8eaf6', 'text_color': '#1a1a4a', 'editor_bg': '#f5f5ff',
        'editor_text': '#1a1a4a', 'border_color': '#9fa8da', 'list_bg': '#f5f5ff',
        'list_text': '#1a1a4a', 'menu_bg': '#e8eaf6', 'menu_text': '#1a1a4a',
        'menu_hover': '#9fa8da', 'button_bg': '#3949ab', 'button_text': '#ffffff',
        'button_hover': '#1a237e', 'progress_bg': '#9fa8da', 'progress_chunk': '#3949ab',
        'scroll_bg': '#9fa8da', 'scroll_handle': '#7986cb', 'scroll_handle_hover': '#5c6bc0'
    },
}

SYNTAX_THEMES = {
    'default': {'keyword': '#569cd6', 'string': '#ce9178', 'comment': '#6a9955', 'function': '#dcdcaa', 'number': '#b5cea8', 'operator': '#d4d4d4', 'class': '#4ec9b0'},
    'monokai': {'keyword': '#f92672', 'string': '#e6db74', 'comment': '#75715e', 'function': '#a6e22e', 'number': '#ae81ff', 'operator': '#f8f8f2', 'class': '#66d9ef'},
    'solarized': {'keyword': '#719e07', 'string': '#2aa198', 'comment': '#93a1a1', 'function': '#268bd2', 'number': '#d33682', 'operator': '#657b83', 'class': '#b58900'},
    'dracula': {'keyword': '#ff79c6', 'string': '#f1fa8c', 'comment': '#6272a4', 'function': '#50fa7b', 'number': '#bd93f9', 'operator': '#f8f8f2', 'class': '#8be9fd'},
    'nord': {'keyword': '#81a1c1', 'string': '#a3be8c', 'comment': '#4c566a', 'function': '#88c0d0', 'number': '#b48ead', 'operator': '#eceff4', 'class': '#5e81ac'},
    'github': {'keyword': '#d73a49', 'string': '#032f62', 'comment': '#6a737d', 'function': '#6f42c1', 'number': '#005cc5', 'operator': '#d73a49', 'class': '#6f42c1'}
}

class LoadingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("ErrorChec")
        self.setFixedSize(400, 250)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        central_widget = QWidget()
        central_widget.setStyleSheet("QWidget { background-color: #1e1e1e; border-radius: 15px; }")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(30, 40, 30, 40)
        central_widget.setLayout(layout)
        
        title_label = QLabel("ErrorChec")
        title_font = QFont("Arial", 32, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white; background-color: transparent;")
        layout.addWidget(title_label)
        
        layout.addSpacing(10)
        
        team_label = QLabel('<a href="https://cadteam.ru" style="color: #3498db; text-decoration: none; font-size: 11px;">Ctrl+Alt+Deleted Team</a>')
        team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        team_label.setOpenExternalLinks(True)
        team_label.setStyleSheet("QLabel { background-color: transparent; }")
        layout.addWidget(team_label)
        
        layout.addSpacing(20)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar { border: none; background-color: #2d2d2d; border-radius: 4px; height: 10px; }
            QProgressBar::chunk { background-color: #3498db; border-radius: 4px; }
        """)
        layout.addWidget(self.progress_bar)
        
        self.start_loading()
        
    def start_loading(self):
        self.loader = LoaderThread()
        self.loader.progress_updated.connect(self.update_progress)
        self.loader.loading_finished.connect(self.on_loading_finished)
        self.loader.start()
        
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
    def on_loading_finished(self):
        QTimer.singleShot(500, self.close)
        self.run_main_app()
        
    def run_main_app(self):
        self.main_window = MainWindow()
        self.main_window.show()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        shadow_color = QColor(0, 0, 0, 50)
        painter.setBrush(QBrush(shadow_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(10, 10, self.width() - 20, self.height() - 20, 15, 15)

class LoaderThread(QThread):
    progress_updated = pyqtSignal(int)
    loading_finished = pyqtSignal()
    
    def run(self):
        total_time = random.uniform(5, 8)
        steps = 100
        step_time = total_time / steps
        
        for i in range(steps + 1):
            if i % 5 == 0:
                self.progress_updated.emit(i)
            sleep_time = step_time * random.uniform(0.8, 1.2)
            time.sleep(sleep_time)
        
        self.progress_updated.emit(100)
        self.loading_finished.emit()

class CompilerManager:
    def __init__(self):
        self.compilers = {
            'php': {'name': 'PHP', 'check': 'php -v', 'install': True},
            'python': {'name': 'Python', 'check': 'python --version', 'install': False},
            'javascript': {'name': 'Node.js', 'check': 'node --version', 'install': True},
            'java': {'name': 'Java JDK', 'check': 'javac -version', 'install': True},
            'csharp': {'name': '.NET Core', 'check': 'dotnet --version', 'install': True},
            'cpp': {'name': 'MinGW-w64', 'check': 'g++ --version', 'install': True},
            'ruby': {'name': 'Ruby', 'check': 'ruby --version', 'install': True},
            'go': {'name': 'Go', 'check': 'go version', 'install': True},
            'rust': {'name': 'Rust', 'check': 'rustc --version', 'install': True},
            'swift': {'name': 'Swift', 'check': 'swift --version', 'install': False}
        }
        self.status = {}
        self.check_all()
    
    def check_all(self):
        for key in self.compilers:
            self.status[key] = self.check_compiler(key)
    
    def check_compiler(self, language):
        check_cmd = self.compilers[language]['check']
        try:
            result = subprocess.run(check_cmd.split(), capture_output=True, text=True, timeout=5, shell=True)
            return result.returncode == 0
        except:
            return False
    
    def is_installed(self, language):
        return self.status.get(language, False)

class CompilerSettingsDialog(QDialog):
    def __init__(self, compiler_manager, parent=None):
        super().__init__(parent)
        self.compiler_manager = compiler_manager
        self.setWindowTitle("Настройки компиляторов")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        header = QLabel("Управление компиляторами")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        layout.addSpacing(10)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        
        for key, compiler in self.compiler_manager.compilers.items():
            group = QGroupBox(compiler['name'])
            group_layout = QVBoxLayout()
            
            status_layout = QHBoxLayout()
            status_label = QLabel("Статус:")
            status_label.setStyleSheet("font-weight: bold;")
            status_layout.addWidget(status_label)
            
            status_text = QLabel("Установлен" if self.compiler_manager.is_installed(key) else "Не установлен")
            status_text.setStyleSheet("color: #27ae60; font-weight: bold;" if self.compiler_manager.is_installed(key) else "color: #e74c3c; font-weight: bold;")
            status_layout.addWidget(status_text)
            status_layout.addStretch()
            group_layout.addLayout(status_layout)
            
            check_btn = QPushButton("Проверить статус")
            check_btn.clicked.connect(lambda checked, k=key: self.check_status(k))
            group_layout.addWidget(check_btn)
            
            if not self.compiler_manager.is_installed(key) and compiler['install']:
                install_btn = QPushButton("Установить")
                install_btn.clicked.connect(lambda checked, k=key: self.install_compiler(k))
                group_layout.addWidget(install_btn)
            
            group.setLayout(group_layout)
            scroll_layout.addWidget(group)
        
        layout.addWidget(scroll)
        
        refresh_btn = QPushButton("Обновить статус всех")
        refresh_btn.clicked.connect(self.refresh_all)
        layout.addWidget(refresh_btn)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btn_box.accepted.connect(self.accept)
        layout.addWidget(btn_box)
        
        self.setLayout(layout)
    
    def check_status(self, language):
        status = self.compiler_manager.check_compiler(language)
        self.compiler_manager.status[language] = status
        self.refresh_all()
    
    def refresh_all(self):
        self.compiler_manager.check_all()
        self.accept()
        new_dialog = CompilerSettingsDialog(self.compiler_manager, self.parent())
        new_dialog.exec()
    
    def install_compiler(self, language):
        QMessageBox.information(self, "Установка", f"Установка {self.compiler_manager.compilers[language]['name']}...\nСледуйте инструкциям установщика.")

class CodeValidator(QThread):
    finished = pyqtSignal(dict)
    compiler_missing = pyqtSignal(str)
    
    def __init__(self, code, language, compiler_manager):
        super().__init__()
        self.code = code
        self.language = language
        self.compiler_manager = compiler_manager
        
    def run(self):
        errors = {}
        
        if self.language == 'python':
            errors = self.validate_python()
        elif self.language == 'php':
            if self.compiler_manager.is_installed('php'):
                errors = self.validate_php()
            else:
                self.compiler_missing.emit('php')
                errors = self.validate_generic()
        elif self.language == 'javascript':
            if self.compiler_manager.is_installed('javascript'):
                errors = self.validate_javascript()
            else:
                self.compiler_missing.emit('javascript')
                errors = self.validate_generic()
        elif self.language == 'java':
            if self.compiler_manager.is_installed('java'):
                errors = self.validate_java()
            else:
                self.compiler_missing.emit('java')
                errors = self.validate_generic()
        elif self.language == 'cpp':
            if self.compiler_manager.is_installed('cpp'):
                errors = self.validate_cpp()
            else:
                self.compiler_missing.emit('cpp')
                errors = self.validate_generic()
        else:
            errors = self.validate_generic()
        
        self.finished.emit(errors)
    
    def validate_python(self):
        errors = {}
        try:
            compile(self.code, '<string>', 'exec')
        except SyntaxError as e:
            errors[e.lineno] = f"Синтаксическая ошибка: {e.msg}"
        
        lines = self.code.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                continue
            if '\t' in line and '    ' in line:
                errors[i] = "Смешивание табов и пробелов"
            if stripped.count('(') != stripped.count(')'):
                errors[i] = "Незакрытые скобки"
        return errors
    
    def validate_php(self):
        errors = {}
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.php', delete=False) as f:
                f.write(self.code)
                temp_file = f.name
            
            result = subprocess.run(['php', '-l', temp_file], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                for line in result.stderr.split('\n'):
                    if 'Parse error' in line:
                        match = re.search(r'line (\d+)', line)
                        if match:
                            errors[int(match.group(1))] = line.strip()
            os.unlink(temp_file)
        except:
            pass
        return errors
    
    def validate_javascript(self):
        errors = {}
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(self.code)
                temp_file = f.name
            
            result = subprocess.run(['node', '--check', temp_file], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                for line in result.stderr.split('\n'):
                    if 'SyntaxError' in line:
                        match = re.search(r':(\d+):', line)
                        if match:
                            errors[int(match.group(1))] = line.strip()
            os.unlink(temp_file)
        except:
            pass
        return errors
    
    def validate_java(self):
        errors = {}
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
                f.write(self.code)
                temp_file = f.name
            
            result = subprocess.run(['javac', '-Xlint:none', temp_file], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                for line in result.stderr.split('\n'):
                    if '.java:' in line:
                        match = re.search(r':(\d+):', line)
                        if match:
                            errors[int(match.group(1))] = line.strip()
            os.unlink(temp_file)
        except:
            pass
        return errors
    
    def validate_cpp(self):
        errors = {}
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                f.write(self.code)
                temp_file = f.name
            
            result = subprocess.run(['g++', '-fsyntax-only', temp_file], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                for line in result.stderr.split('\n'):
                    if '.cpp:' in line:
                        match = re.search(r':(\d+):', line)
                        if match:
                            errors[int(match.group(1))] = line.strip()
            os.unlink(temp_file)
        except:
            pass
        return errors
    
    def validate_generic(self):
        errors = {}
        lines = self.code.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.count('(') != stripped.count(')'):
                errors[i] = "Несоответствие круглых скобок"
            if stripped.count('[') != stripped.count(']'):
                errors[i] = "Несоответствие квадратных скобок"
            if stripped.count('{') != stripped.count('}'):
                errors[i] = "Несоответствие фигурных скобок"
            if stripped.count('"') % 2 != 0 or stripped.count("'") % 2 != 0:
                errors[i] = "Незакрытая кавычка"
        return errors

class CodeHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, language='python', theme='default'):
        super().__init__(parent)
        self.language = language
        self.theme = theme
        self.highlighting_rules = []
        self.error_lines = []
        self.setup_rules()
    
    def setup_rules(self):
        self.highlighting_rules = []
        theme = SYNTAX_THEMES.get(self.theme, SYNTAX_THEMES['default'])
        
        keyword_color = QColor(theme['keyword'])
        string_color = QColor(theme['string'])
        comment_color = QColor(theme['comment'])
        function_color = QColor(theme['function'])
        number_color = QColor(theme['number'])
        operator_color = QColor(theme['operator'])
        class_color = QColor(theme['class'])
        
        rules = []
        rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_color))
        rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_color))
        rules.append((QRegularExpression(r'//[^\n]*'), comment_color))
        rules.append((QRegularExpression(r'#[^\n]*'), comment_color))
        rules.append((QRegularExpression(r'/\*.*?\*/'), comment_color))
        rules.append((QRegularExpression(r'\b[0-9]+\b'), number_color))
        rules.append((QRegularExpression(r'[+\-*/=<>!&|%^~]'), operator_color))
        
        keywords = ['if','else','for','while','return','def','class','import','try','except','break','continue']
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
        rules.append((QRegularExpression(pattern), keyword_color))
        rules.append((QRegularExpression(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\('), function_color))
        rules.append((QRegularExpression(r'\b([A-Z][a-zA-Z0-9_]*)\b'), class_color))
        
        for pattern, color in rules:
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.highlighting_rules.append((pattern, fmt))
    
    def set_error_lines(self, error_lines):
        self.error_lines = error_lines
        self.rehighlight()
    
    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
        
        block_number = self.currentBlock().blockNumber() + 1
        if block_number in self.error_lines:
            fmt = QTextCharFormat()
            fmt.setBackground(QColor(255, 50, 50, 80))
            self.setFormat(0, len(text), fmt)

class LanguageDialog(QDialog):
    def __init__(self, detected_lang, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Определение языка")
        self.setModal(True)
        self.setFixedSize(450, 200)
        
        layout = QVBoxLayout()
        label = QLabel("Правильно ли определен язык?")
        label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label)
        
        if detected_lang:
            lang_label = QLabel(f"Язык: {detected_lang.upper()}")
            lang_label.setStyleSheet("font-size: 18px; color: #3498db; font-weight: bold;")
            layout.addWidget(lang_label)
        
        layout.addSpacing(20)
        
        btn_layout = QHBoxLayout()
        self.btn_yes = QPushButton("Да")
        self.btn_yes.clicked.connect(self.accept)
        self.btn_no = QPushButton("Нет, выбрать самому")
        self.btn_no.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_yes)
        btn_layout.addWidget(self.btn_no)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

class LanguageSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выберите язык")
        self.setModal(True)
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        label = QLabel("Выберите язык программирования:")
        layout.addWidget(label)
        
        self.lang_combo = QComboBox()
        languages = ['python', 'php', 'javascript', 'java', 'cpp', 'ruby', 'go', 'rust', 'swift', 'html', 'css']
        self.lang_combo.addItems(languages)
        layout.addWidget(self.lang_combo)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        
        self.setLayout(layout)
    
    def get_language(self):
        return self.lang_combo.currentText()

class BackupIntervalDialog(QDialog):
    def __init__(self, current_interval, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройка интервала резервного копирования")
        self.setModal(True)
        self.setFixedSize(350, 150)
        
        layout = QVBoxLayout()
        label = QLabel("Интервал резервного копирования (секунд):")
        layout.addWidget(label)
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(10, 3600)
        self.interval_spin.setValue(current_interval)
        self.interval_spin.setSuffix(" сек")
        layout.addWidget(self.interval_spin)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        
        self.setLayout(layout)
    
    def get_interval(self):
        return self.interval_spin.value()

class CompilerDialog(QDialog):
    def __init__(self, language, compiler_manager, parent=None):
        super().__init__(parent)
        self.language = language
        self.compiler_manager = compiler_manager
        self.setWindowTitle("Установка компилятора")
        self.setModal(True)
        self.setFixedSize(450, 180)
        
        layout = QVBoxLayout()
        lang_name = self.compiler_manager.compilers[language]['name']
        label = QLabel(f"Компилятор для {lang_name} не установлен")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c;")
        layout.addWidget(label)
        
        info_label = QLabel("Некоторые ошибки могут не определяться")
        info_label.setStyleSheet("color: #888;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        if self.compiler_manager.compilers[language]['install']:
            install_btn = QPushButton("Установить компилятор")
            install_btn.clicked.connect(lambda: QMessageBox.information(self, "Установка", f"Установите {lang_name} с официального сайта"))
            layout.addWidget(install_btn)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btn_box.accepted.connect(self.accept)
        layout.addWidget(btn_box)
        
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.current_language = 'python'
        self.errors = {}
        self.backup_enabled = True
        self.backup_interval = 300
        self.settings_file = "settings.json"
        self.current_theme = "dark_01"
        self.syntax_theme = "default"
        self.highlighter = None
        self.validator = None
        self.compiler_manager = CompilerManager()
        self.load_settings()
        
        self.init_ui()
        self.apply_theme()
        self.setup_highlighter()
        
        self.backup_timer = QTimer()
        self.backup_timer.timeout.connect(self.create_backup)
        if self.backup_enabled:
            self.backup_timer.start(self.backup_interval * 1000)
        
    def setup_highlighter(self):
        if self.highlighter:
            self.highlighter.setDocument(None)
        self.highlighter = CodeHighlighter(
            self.code_editor.document(),
            self.current_language,
            self.syntax_theme
        )
        
    def init_ui(self):
        self.setWindowTitle("ErrorChec - Анализатор кода")
        self.setGeometry(100, 100, 1200, 800)
        
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("Файл")
        open_action = QAction("Открыть", self)
        open_action.triggered.connect(self.open_file)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_file)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Сохранить как", self)
        save_as_action.triggered.connect(self.save_file_as)
        save_as_action.setShortcut("Ctrl+Shift+S")
        file_menu.addAction(save_as_action)
        
        encoding_menu = menubar.addMenu("Кодировка")
        encodings = ['UTF-8', 'UTF-16', 'CP1251', 'ISO-8859-1', 'ASCII', 'KOI8-R']
        for enc in encodings:
            action = QAction(enc, self)
            action.triggered.connect(lambda checked, e=enc: self.change_encoding(e))
            encoding_menu.addAction(action)
        
        settings_menu = menubar.addMenu("Настройки")
        
        view_menu = QMenu("Вид", self)
        settings_menu.addMenu(view_menu)
        
        theme_menu = QMenu("Темы", self)
        view_menu.addMenu(theme_menu)
        
        dark_menu = QMenu("Темные темы", self)
        theme_menu.addMenu(dark_menu)
        for theme in sorted([t for t in THEMES.keys() if 'dark' in t]):
            action = QAction(theme.replace('_', ' ').title(), self)
            action.triggered.connect(lambda checked, t=theme: self.apply_theme(t))
            dark_menu.addAction(action)
        
        light_menu = QMenu("Светлые темы", self)
        theme_menu.addMenu(light_menu)
        for theme in sorted([t for t in THEMES.keys() if 'light' in t]):
            action = QAction(theme.replace('_', ' ').title(), self)
            action.triggered.connect(lambda checked, t=theme: self.apply_theme(t))
            light_menu.addAction(action)
        
        syntax_menu = QMenu("Подсветка синтаксиса", self)
        view_menu.addMenu(syntax_menu)
        for theme in SYNTAX_THEMES:
            action = QAction(theme.replace('_', ' ').title(), self)
            action.triggered.connect(lambda checked, t=theme: self.apply_syntax_theme(t))
            syntax_menu.addAction(action)
        
        compilers_action = QAction("Компиляторы", self)
        compilers_action.triggered.connect(self.show_compiler_settings)
        settings_menu.addAction(compilers_action)
        
        backup_menu = QMenu("Резервное копирование", self)
        settings_menu.addMenu(backup_menu)
        
        self.backup_action = QAction("Включить резервное копирование", self)
        self.backup_action.setCheckable(True)
        self.backup_action.setChecked(self.backup_enabled)
        self.backup_action.triggered.connect(self.toggle_backup)
        backup_menu.addAction(self.backup_action)
        
        backup_interval_action = QAction("Настроить интервал", self)
        backup_interval_action.triggered.connect(self.set_backup_interval)
        backup_menu.addAction(backup_interval_action)
        
        resources_menu = QMenu("Ресурсы", self)
        settings_menu.addMenu(resources_menu)
        resources_action = QAction("Потребление памяти", self)
        resources_action.triggered.connect(self.show_resources)
        resources_menu.addAction(resources_action)
        
        settings_menu.addSeparator()
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Ctrl+Q")
        settings_menu.addAction(exit_action)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        
        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont("Consolas", 12))
        self.code_editor.textChanged.connect(self.on_text_changed)
        left_layout.addWidget(self.code_editor)
        splitter.addWidget(left_widget)
        
        right_widget = QWidget()
        right_widget.setMaximumWidth(400)
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        
        errors_label = QLabel("Ошибки:")
        errors_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        right_layout.addWidget(errors_label)
        
        self.errors_list = QListWidget()
        self.errors_list.itemClicked.connect(self.go_to_error)
        right_layout.addWidget(self.errors_list)
        
        self.status_label = QLabel("Готов к работе")
        self.status_label.setStyleSheet("color: #888; font-size: 11px;")
        right_layout.addWidget(self.status_label)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([800, 400])
        
        self.analyze_timer = QTimer()
        self.analyze_timer.setSingleShot(True)
        self.analyze_timer.timeout.connect(self.analyze_code)
    
    def load_settings(self):
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                self.backup_enabled = settings.get('backup_enabled', True)
                self.backup_interval = settings.get('backup_interval', 300)
                self.current_theme = settings.get('theme', 'dark_01')
                self.syntax_theme = settings.get('syntax_theme', 'default')
        except:
            pass
    
    def save_settings(self):
        settings = {
            'backup_enabled': self.backup_enabled,
            'backup_interval': self.backup_interval,
            'theme': self.current_theme,
            'syntax_theme': self.syntax_theme
        }
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
        except:
            pass
    
    def apply_theme(self, theme_name=None):
        if theme_name:
            self.current_theme = theme_name
        theme = THEMES.get(self.current_theme, THEMES['dark_01'])
        
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {theme['bg_color']};
                color: {theme['text_color']};
            }}
            QTextEdit {{
                background-color: {theme['editor_bg']};
                color: {theme['editor_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 5px;
            }}
            QListWidget {{
                background-color: {theme['list_bg']};
                color: {theme['list_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 5px;
            }}
            QMenuBar {{
                background-color: {theme['menu_bg']};
                color: {theme['menu_text']};
            }}
            QMenuBar::item:selected {{
                background-color: {theme['menu_hover']};
            }}
            QMenu {{
                background-color: {theme['menu_bg']};
                color: {theme['menu_text']};
                border: 1px solid {theme['border_color']};
            }}
            QMenu::item:selected {{
                background-color: {theme['menu_hover']};
            }}
            QPushButton {{
                background-color: {theme['button_bg']};
                color: {theme['button_text']};
                border: none;
                padding: 8px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
            }}
            QProgressBar {{
                background-color: {theme['progress_bg']};
                border: none;
                border-radius: 4px;
                height: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {theme['progress_chunk']};
                border-radius: 4px;
            }}
            QScrollBar:vertical {{
                background-color: {theme['scroll_bg']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {theme['scroll_handle']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {theme['scroll_handle_hover']};
            }}
            QScrollBar:horizontal {{
                background-color: {theme['scroll_bg']};
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {theme['scroll_handle']};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {theme['scroll_handle_hover']};
            }}
            QLabel {{
                color: {theme['text_color']};
            }}
            QGroupBox {{
                border: 1px solid {theme['border_color']};
                border-radius: 5px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
        self.save_settings()
    
    def apply_syntax_theme(self, theme_name):
        self.syntax_theme = theme_name
        self.save_settings()
        self.setup_highlighter()
        self.code_editor.document().setPlainText(self.code_editor.toPlainText())
    
    def on_text_changed(self):
        self.analyze_timer.start(500)
    
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Все файлы (*.*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.code_editor.setText(code)
                self.current_file = file_path
                self.detect_language(code)
                self.setup_highlighter()
                self.analyze_code()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")
    
    def detect_language(self, code):
        if self.current_file:
            ext = os.path.splitext(self.current_file)[1].lower()
            lang_map = {
                '.py': 'python', '.php': 'php', '.js': 'javascript',
                '.java': 'java', '.cpp': 'cpp', '.rb': 'ruby',
                '.go': 'go', '.rs': 'rust', '.swift': 'swift',
                '.html': 'html', '.css': 'css'
            }
            detected = lang_map.get(ext)
            if detected:
                dialog = LanguageDialog(detected, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.current_language = detected
                    self.setup_highlighter()
                else:
                    selector = LanguageSelectorDialog(self)
                    if selector.exec() == QDialog.DialogCode.Accepted:
                        self.current_language = selector.get_language()
                        self.setup_highlighter()
            else:
                selector = LanguageSelectorDialog(self)
                if selector.exec() == QDialog.DialogCode.Accepted:
                    self.current_language = selector.get_language()
                    self.setup_highlighter()
    
    def analyze_code(self):
        code = self.code_editor.toPlainText()
        if not code.strip() or not self.current_language:
            self.errors_list.clear()
            self.status_label.setText("Нет кода для анализа")
            return
        
        self.status_label.setText("Анализ кода...")
        if self.validator and self.validator.isRunning():
            self.validator.terminate()
        
        self.validator = CodeValidator(code, self.current_language, self.compiler_manager)
        self.validator.finished.connect(self.on_validation_finished)
        self.validator.compiler_missing.connect(self.on_compiler_missing)
        self.validator.start()
    
    def on_validation_finished(self, errors):
        self.errors = errors
        self.errors_list.clear()
        
        if errors:
            unique_errors = {}
            for line, error in errors.items():
                if line not in unique_errors:
                    unique_errors[line] = error
            
            for line, error in unique_errors.items():
                item = QListWidgetItem(f"Строка {line}: {error}")
                item.setData(Qt.ItemDataRole.UserRole, line)
                self.errors_list.addItem(item)
            
            self.status_label.setText(f"Найдено {len(unique_errors)} ошибок")
            self.highlighter.set_error_lines(list(unique_errors.keys()))
        else:
            self.status_label.setText("Ошибок не найдено")
            self.highlighter.set_error_lines([])
    
    def on_compiler_missing(self, language):
        dialog = CompilerDialog(language, self.compiler_manager, self)
        dialog.exec()
    
    def show_compiler_settings(self):
        dialog = CompilerSettingsDialog(self.compiler_manager, self)
        dialog.exec()
    
    def go_to_error(self, item):
        line = item.data(Qt.ItemDataRole.UserRole)
        if line:
            cursor = self.code_editor.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            for _ in range(line - 1):
                cursor.movePosition(QTextCursor.MoveOperation.Down)
            self.code_editor.setTextCursor(cursor)
            self.code_editor.setFocus()
    
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.code_editor.toPlainText())
                QMessageBox.information(self, "Успех", "Файл сохранен!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        extensions = {
            'python': 'py', 'php': 'php', 'javascript': 'js',
            'java': 'java', 'cpp': 'cpp', 'ruby': 'rb',
            'go': 'go', 'rust': 'rs', 'swift': 'swift',
            'html': 'html', 'css': 'css'
        }
        ext = extensions.get(self.current_language, 'txt')
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", f"untitled.{ext}",
            f"{self.current_language.upper() if self.current_language else 'Text'} files (*.{ext})"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.code_editor.toPlainText())
                self.current_file = file_path
                QMessageBox.information(self, "Успех", "Файл сохранен!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def change_encoding(self, encoding):
        try:
            text = self.code_editor.toPlainText()
            encoded = text.encode(encoding)
            self.code_editor.setText(encoded.decode(encoding))
            QMessageBox.information(self, "Успех", f"Кодировка изменена на {encoding}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось изменить кодировку: {str(e)}")
    
    def toggle_backup(self):
        self.backup_enabled = not self.backup_enabled
        self.backup_action.setChecked(self.backup_enabled)
        
        if self.backup_enabled:
            self.backup_timer.start(self.backup_interval * 1000)
            QMessageBox.information(self, "Бэкап", "Резервное копирование включено")
        else:
            self.backup_timer.stop()
            QMessageBox.information(self, "Бэкап", "Резервное копирование отключено")
        self.save_settings()
    
    def set_backup_interval(self):
        dialog = BackupIntervalDialog(self.backup_interval, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.backup_interval = dialog.get_interval()
            self.save_settings()
            if self.backup_enabled:
                self.backup_timer.stop()
                self.backup_timer.start(self.backup_interval * 1000)
            QMessageBox.information(self, "Бэкап", f"Интервал установлен на {self.backup_interval} секунд")
    
    def create_backup(self):
        if self.backup_enabled and self.code_editor.toPlainText():
            try:
                backup_dir = "backups"
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(backup_dir, f"backup_{timestamp}.txt")
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(self.code_editor.toPlainText())
            except Exception as e:
                print(f"Ошибка бэкапа: {e}")
    
    def show_resources(self):
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            QMessageBox.information(
                self,
                "Потребление ресурсов",
                f"Память: {memory_info.rss / 1024 / 1024:.2f} MB\n"
                f"CPU: {process.cpu_percent()}%\n"
                f"Открыто файлов: {len(process.open_files())}"
            )
        except ImportError:
            QMessageBox.warning(self, "Ошибка", "Установите psutil: pip install psutil")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось получить информацию: {str(e)}")

def main():
    freeze_support()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    loading = LoadingWindow()
    loading.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()