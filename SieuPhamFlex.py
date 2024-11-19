import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout,
    QScrollArea, QMessageBox, QSpinBox, QComboBox, QGraphicsDropShadowEffect, QDialog
)
from PyQt5.QtGui import QPixmap, QMouseEvent, QPainter, QColor
from PyQt5.QtCore import Qt, QCoreApplication

import unittest
from collections import defaultdict
import itertools
import json
import os
from sklearn.neighbors import NearestNeighbors
import numpy as np
import random
import requests

VERSION = "1.0.0"
REPO_OWNER = "jerrylemin"  # Thay bằng tên người dùng GitHub của bạn
REPO_NAME = "FLEXTFT"     # Thay bằng tên repository của bạn

def resource_path(relative_path):
    """Tìm đường dẫn tới tệp dữ liệu, hoạt động cả khi chạy dưới dạng script hoặc exe."""
    try:
        # Nếu chạy dưới dạng exe
        base_path = sys._MEIPASS
    except Exception:
        # Nếu chạy dưới dạng script
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Dữ liệu Champions
champions = [
    {"Name": "Lux", "Cost": 1, "Tộc Hệ": ["Học Viện", "Phù Thủy"], "Icon": "icons/Lux.png"},
    {"Name": "Leona", "Cost": 2, "Tộc Hệ": ["Học Viện", "Vệ Binh"], "Icon": "icons/Leona.png"},
    {"Name": "Ezreal", "Cost": 3, "Tộc Hệ": ["Học Viện", "Nổi Loạn", "Pháo Binh"], "Icon": "icons/Ezreal.png"},
    {"Name": "Heimer", "Cost": 4, "Tộc Hệ": ["Học Viện", "Tiên Tri"], "Icon": "icons/Heimerdinger.png"},
    {"Name": "Jayce", "Cost": 5, "Tộc Hệ": ["Học Viện", "Song Hình"], "Icon": "icons/Jayce.png"},
    {"Name": "Amumu", "Cost": 1, "Tộc Hệ": ["Cỗ Máy Tự Động", "Giám Sát"], "Icon": "icons/Amumu.png"},
    {"Name": "Nocturne", "Cost": 2, "Tộc Hệ": ["Cỗ Máy Tự Động", "Cực Tốc"], "Icon": "icons/Nocturne.png"},
    {"Name": "Kog'Maw", "Cost": 3, "Tộc Hệ": ["Cỗ Máy Tự Động", "Bắn Tỉa"], "Icon": "icons/KogMaw.png"},
    {"Name": "Blitzcrank", "Cost": 3, "Tộc Hệ": ["Cỗ Máy Tự Động", "Thống Trị"], "Icon": "icons/Blitzcrank.png"},
    {"Name": "Malzahar", "Cost": 5, "Tộc Hệ": ["Cỗ Máy Tự Động", "Tiên Tri"], "Icon": "icons/Malzahar.png"},
    {"Name": "Morgana", "Cost": 1, "Tộc Hệ": ["Hoa Hồng Đen", "Tiên Tri"], "Icon": "icons/Morgana.png"},
    {"Name": "Vladimir", "Cost": 2, "Tộc Hệ": ["Hoa Hồng Đen", "Phù Thủy", "Giám Sát"], "Icon": "icons/Vladimir.png"},
    {"Name": "Cassiopeia", "Cost": 3, "Tộc Hệ": ["Hoa Hồng Đen", "Thống Trị"], "Icon": "icons/Cassiopeia.png"},
    {"Name": "Elise", "Cost": 4, "Tộc Hệ": ["Hoa Hồng Đen", "Song Hình", "Đấu Sĩ"], "Icon": "icons/Elise.png"},
    {"Name": "LeBlanc", "Cost": 5, "Tộc Hệ": ["Hoa Hồng Đen", "Phù Thủy"], "Icon": "icons/LeBlanc.png"},
    {"Name": "Singed", "Cost": 1, "Tộc Hệ": ["Hóa Chủ", "Vệ Binh"], "Icon": "icons/Singed.png"},
    {"Name": "Renata Glasc", "Cost": 2, "Tộc Hệ": ["Hóa Chủ", "Tiên Tri"], "Icon": "icons/RenataGlasc.png"},
    {"Name": "Smeech", "Cost": 3, "Tộc Hệ": ["Hóa Chủ", "Phục Kích"], "Icon": "icons/Smeech.png"},
    {"Name": "Renni", "Cost": 3, "Tộc Hệ": ["Hóa Chủ", "Đấu Sĩ"], "Icon": "icons/Renni.png"},
    {"Name": "Silco", "Cost": 4, "Tộc Hệ": ["Hóa Chủ", "Thống Trị"], "Icon": "icons/Silco.png"},
    {"Name": "Sevika", "Cost": 5, "Tộc Hệ": ["Tay Bạc", "Hóa Chủ", "Võ Sĩ Lồng Sắt"], "Icon": "icons/Sevika.png"},
    {"Name": "Darius", "Cost": 1, "Tộc Hệ": ["Chinh Phục", "Giám Sát"], "Icon": "icons/Darius.png"},
    {"Name": "Draven", "Cost": 1, "Tộc Hệ": ["Chinh Phục", "Võ Sĩ Lồng Sắt"], "Icon": "icons/Draven.png"},
    {"Name": "Rell", "Cost": 2, "Tộc Hệ": ["Chinh Phục", "Vệ Binh", "Tiên Tri"], "Icon": "icons/Rell.png"},
    {"Name": "Swain", "Cost": 3, "Tộc Hệ": ["Chinh Phục", "Song Hình", "Phù Thủy"], "Icon": "icons/Swain.png"},
    {"Name": "Ambessa", "Cost": 4, "Tộc Hệ": ["Sứ Giả", "Chinh Phục", "Cực Tốc"], "Icon": "icons/Ambessa.png"},
    {"Name": "Mordekaiser", "Cost": 5, "Tộc Hệ": ["Chinh Phục", "Thống Trị"], "Icon": "icons/Mordekaiser.png"},
    {"Name": "Tristana", "Cost": 2, "Tộc Hệ": ["Sứ Giả", "Pháo Binh"], "Icon": "icons/Tristana.png"},
    {"Name": "Nami", "Cost": 3, "Tộc Hệ": ["Sứ Giả", "Phù Thủy"], "Icon": "icons/Nami.png"},
    {"Name": "Garen", "Cost": 4, "Tộc Hệ": ["Sứ Giả", "Giám Sát"], "Icon": "icons/Garen.png"},
    {"Name": "Steb", "Cost": 1, "Tộc Hệ": ["Cảnh Binh", "Đấu Sĩ"], "Icon": "icons/Steb.png"},
    {"Name": "Maddie", "Cost": 1, "Tộc Hệ": ["Cảnh Binh", "Bắn Tỉa"], "Icon": "icons/Maddie.png"},
    {"Name": "Camille", "Cost": 2, "Tộc Hệ": ["Cảnh Binh", "Phục Kích"], "Icon": "icons/Camille.png"},
    {"Name": "Twisted Fate", "Cost": 3, "Tộc Hệ": ["Cảnh Binh", "Cực Tốc"], "Icon": "icons/TwistedFate.png"},
    {"Name": "Loris", "Cost": 3, "Tộc Hệ": ["Cảnh Binh", "Vệ Binh"], "Icon": "icons/Loris.png"},
    {"Name": "Vi", "Cost": 4, "Tộc Hệ": ["Cảnh Binh", "Võ Sĩ Lồng Sắt"], "Icon": "icons/Vi.png"},
    {"Name": "Zyra", "Cost": 1, "Tộc Hệ": ["Thí Nghiệm", "Phù Thủy"], "Icon": "icons/Zyra.png"},
    {"Name": "Urgot", "Cost": 2, "Tộc Hệ": ["Thí Nghiệm", "Võ Sĩ Lồng Sắt", "Pháo Binh"], "Icon": "icons/Urgot.png"},
    {"Name": "Nunu", "Cost": 3, "Tộc Hệ": ["Thí Nghiệm", "Đấu Sĩ", "Tiên Tri"], "Icon": "icons/NunuWillump.png"},
    {"Name": "Dr. Mundo", "Cost": 4, "Tộc Hệ": ["Thí Nghiệm", "Thống Trị"], "Icon": "icons/DrMundo.png"},
    {"Name": "Twitch", "Cost": 4, "Tộc Hệ": ["Thí Nghiệm", "Bắn Tỉa"], "Icon": "icons/Twitch.png"},
    {"Name": "Powder", "Cost": 1, "Tộc Hệ": ["Gia Đình", "Tái Chế", "Phục Kích"], "Icon": "icons/Powder.png"},
    {"Name": "Violet", "Cost": 1, "Tộc Hệ": ["Gia Đình", "Võ Sĩ Lồng Sắt"], "Icon": "icons/Violet.png"},
    {"Name": "Vander", "Cost": 2, "Tộc Hệ": ["Gia Đình", "Giám Sát"], "Icon": "icons/Vander.png"},
    {"Name": "Zeri", "Cost": 2, "Tộc Hệ": ["Ánh Lửa", "Bắn Tỉa"], "Icon": "icons/Zeri.png"},
    {"Name": "Scar", "Cost": 3, "Tộc Hệ": ["Ánh Lửa", "Giám Sát"], "Icon": "icons/Scar.png"},
    {"Name": "Ekko", "Cost": 4, "Tộc Hệ": ["Ánh Lửa", "Tái Chế", "Phục Kích"], "Icon": "icons/Ekko.png"},
    {"Name": "Rumble", "Cost": 5, "Tộc Hệ": ["Vua Phế Liệu", "Tái Chế", "Vệ Binh"], "Icon": "icons/Rumble.png"},
    {"Name": "Vex", "Cost": 1, "Tộc Hệ": ["Nổi Loạn", "Tiên Tri"], "Icon": "icons/Vex.png"},
    {"Name": "Irelia", "Cost": 1, "Tộc Hệ": ["Nổi Loạn", "Vệ Binh"], "Icon": "icons/Irelia.png"},
    {"Name": "Sett", "Cost": 2, "Tộc Hệ": ["Nổi Loạn", "Đấu Sĩ"], "Icon": "icons/Sett.png"},
    {"Name": "Akali", "Cost": 2, "Tộc Hệ": ["Nổi Loạn", "Cực Tốc"], "Icon": "icons/Akali.png"},
    {"Name": "Illaoi", "Cost": 4, "Tộc Hệ": ["Nổi Loạn", "Vệ Binh"], "Icon": "icons/Illaoi.png"},
    {"Name": "Zoe", "Cost": 4, "Tộc Hệ": ["Nổi Loạn", "Phù Thủy"], "Icon": "icons/Zoe.png"},
    {"Name": "Jinx", "Cost": 5, "Tộc Hệ": ["Nổi Loạn", "Phục Kích"], "Icon": "icons/Jinx.png"},
    {"Name": "Trundle", "Cost": 1, "Tộc Hệ": ["Tái Chế", "Đấu Sĩ"], "Icon": "icons/Trundle.png"},
    {"Name": "Ziggs", "Cost": 2, "Tộc Hệ": ["Tái Chế", "Thống Trị"], "Icon": "icons/Ziggs.png"},
    {"Name": "Gangplank", "Cost": 3, "Tộc Hệ": ["Tái Chế", "Song Hình", "Võ Sĩ Lồng Sắt"], "Icon": "icons/Gangplank.png"},
    {"Name": "Corki", "Cost": 4, "Tộc Hệ": ["Tái Chế", "Pháo Binh"], "Icon": "icons/Corki.png"},
    {"Name": "Caitlyn", "Cost": 5, "Tộc Hệ": ["Cảnh Binh", "Bắn Tỉa"], "Icon": "icons/Caitlyn.png"},
]

# Dữ liệu Tộc Hệ
traits_active = {
    "Bắn Tỉa": [2, 4, 6],
    "Chinh Phục": [2, 4, 6, 9],
    "Cảnh Binh": [2, 4, 6, 8, 10],
    "Cỗ Máy Tự Động": [2, 4, 6],
    "Cực Tốc": [2, 3, 4],
    "Gia Đình": [3, 4, 5],
    "Giám Sát": [2, 4, 6],
    "Hoa Hồng Đen": [3, 4, 5, 7],
    "Hóa Chủ": [3, 4, 5, 6, 7],
    "Học Viện": [3, 4, 5, 6],
    "Nổi Loạn": [3, 5, 7, 10],
    "Pháo Binh": [2, 4, 6],
    "Phù Thủy": [2, 4, 6, 8],
    "Phục Kích": [2, 3, 4, 5],
    "Song Hình": [2, 4],
    "Sứ Giả": [1, 4],
    "Tay Bạc": [1],
    "Thí Nghiệm": [3, 5, 7],
    "Thống Trị": [2, 4, 6],
    "Tiên Tri": [2, 4, 6, 10],
    "Tái Chế": [2, 4, 6, 9],
    "Vua Phế Liệu": [1],
    "Võ Sĩ Lồng Sắt": [2, 4, 6, 8],
    "Vệ Binh": [2, 4, 6],
    "Ánh Lửa": [2, 3, 4],
    "Đấu Sĩ": [2, 4, 6],
}

# Define traits with their icons
traits = [
    {"Tộc Hệ": "Cảnh Binh", "Icon": ["icons/base.png", "icons/squad.png"]},
    {"Tộc Hệ": "Bắn Tỉa", "Icon": ["icons/base.png", "icons/sniper.png"]},
    {"Tộc Hệ": "Học Viện", "Icon": ["icons/base.png", "icons/academy.png"]},
    {"Tộc Hệ": "Song Hình", "Icon": ["icons/base.png", "icons/formswapper.png"]},
    {"Tộc Hệ": "Nổi Loạn", "Icon": ["icons/base.png", "icons/rebel.png"]},
    {"Tộc Hệ": "Phục Kích", "Icon": ["icons/base.png", "icons/ambusher.png"]},
    {"Tộc Hệ": "Hoa Hồng Đen", "Icon": ["icons/base.png", "icons/cabal.png"]},
    {"Tộc Hệ": "Phù Thủy", "Icon": ["icons/base.png", "icons/sorcerer.png"]},
    {"Tộc Hệ": "Cỗ Máy Tự Động", "Icon": ["icons/base.png", "icons/hextech.png"]},
    {"Tộc Hệ": "Tiên Tri", "Icon": ["icons/base.png", "icons/invoker.png"]},
    {"Tộc Hệ": "Chinh Phục", "Icon": ["icons/base.png", "icons/warband.png"]},
    {"Tộc Hệ": "Thống Trị", "Icon": ["icons/base.png", "icons/infused.png"]},
    {"Tộc Hệ": "Vua Phế Liệu", "Icon": ["icons/base.png", "icons/junkerking.png"]},
    {"Tộc Hệ": "Tái Chế", "Icon": ["icons/base.png", "icons/scrap.png"]},
    {"Tộc Hệ": "Vệ Binh", "Icon": ["icons/base.png", "icons/titan.png"]},
    {"Tộc Hệ": "Tay Bạc", "Icon": ["icons/base.png", "icons/highroller.png"]},
    {"Tộc Hệ": "Hóa Chủ", "Icon": ["icons/base.png", "icons/crime.png"]},
    {"Tộc Hệ": "Võ Sĩ Lồng Sắt", "Icon": ["icons/base.png", "icons/pugilist.png"]},
    {"Tộc Hệ": "Sứ Giả", "Icon": ["icons/base.png", "icons/ambassador.png"]},
    {"Tộc Hệ": "Cực Tốc", "Icon": ["icons/base.png", "icons/challenger.png"]},
    {"Tộc Hệ": "Pháo Binh", "Icon": ["icons/base.png", "icons/martialist.png"]},
    {"Tộc Hệ": "Thí Nghiệm", "Icon": ["icons/base.png", "icons/experiment.png"]},
    {"Tộc Hệ": "Ánh Lửa", "Icon": ["icons/base.png", "icons/hoverboard.png"]},
    {"Tộc Hệ": "Giám Sát", "Icon": ["icons/base.png", "icons/watcher.png"]},
    {"Tộc Hệ": "Đấu Sĩ", "Icon": ["icons/base.png", "icons/bruiser.png"]},
    {"Tộc Hệ": "Gia Đình", "Icon": ["icons/base.png", "icons/family.png"]},
]

class FavoriteTeamsWindow(QDialog):
    def __init__(self, team_builder_ai, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Favorite Teams")
        self.setGeometry(150, 150, 800, 600)  # Điều chỉnh kích thước cửa sổ nếu cần
        self.team_builder_ai = team_builder_ai

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Scroll Area để chứa danh sách đội hình
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        scroll_content.setLayout(self.scroll_layout)
        scroll.setWidget(scroll_content)

        self.layout.addWidget(scroll)

        self.populate_favorite_teams()

        # Nút đóng
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.layout.addWidget(close_button)

    def populate_favorite_teams(self):
        """Hiển thị tất cả các đội hình yêu thích với icon tướng và số lượng trait kích hoạt."""
        # Xoá các widget cũ
        self.clear_layout(self.scroll_layout)

        favorite_teams = self.team_builder_ai.favorite_teams
        print(f"Populating favorite teams: {len(favorite_teams)} teams found.")  # Debug

        if not favorite_teams:
            no_team_label = QLabel("Không có đội hình yêu thích nào.")
            no_team_label.setStyleSheet("color: white;")
            self.scroll_layout.addWidget(no_team_label)
            return

        for idx, team_entry in enumerate(favorite_teams):
            print(f"Displaying team {idx + 1}: {team_entry['team']}")  # Debug
            team_widget = QWidget()
            team_layout = QVBoxLayout()
            team_widget.setLayout(team_layout)

            # Thông tin đội hình
            header_layout = QHBoxLayout()
            team_label = QLabel(f"<b>Đội Hình {idx + 1} (Level {team_entry['level']}):</b>")
            team_label.setStyleSheet("color: white;")
            header_layout.addWidget(team_label)
            header_layout.addStretch()

            # Nút xoá
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #b22222;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #cd5c5c;
                }
            """)
            delete_button.clicked.connect(lambda checked, idx=idx: self.delete_team(idx))
            header_layout.addWidget(delete_button)

            team_layout.addLayout(header_layout)

            # Vùng hiển thị các tướng trong đội
            champions_layout = QHBoxLayout()
            for champ_name in team_entry["team"]:
                champ = next((c for c in champions if c["Name"] == champ_name), None)
                if champ:
                    champ_label = ChampionLabel(champ, self)
                    champions_layout.addWidget(champ_label)
                else:
                    # Nếu không tìm thấy tướng, thêm một QLabel trống
                    spacer = QLabel()
                    spacer.setFixedSize(70, 70)
                    champions_layout.addWidget(spacer)
            team_layout.addLayout(champions_layout)

            # Vùng hiển thị các trait đã kích hoạt
            traits_layout = QVBoxLayout()
            traits_label = QLabel("<b>Activated Traits:</b>")
            traits_label.setStyleSheet("color: white;")
            traits_layout.addWidget(traits_label)

            # Tính tổng các trait từ tướng và emblem
            total_traits = defaultdict(int)
            for champ_name in team_entry["team"]:
                champ = next((c for c in champions if c["Name"] == champ_name), None)
                if champ:
                    for trait in champ["Tộc Hệ"]:
                        total_traits[trait] += 1
            for trait, count in team_entry["emblems"].items():
                total_traits[trait] += count

            # Xác định các trait đã được kích hoạt
            activated_traits = {}
            for trait, milestones in traits_active.items():
                # Tìm mốc kích hoạt cao nhất mà đội hình đã đạt
                activated_milestones = [m for m in milestones if total_traits.get(trait, 0) >= m]
                if activated_milestones:
                    activated_traits[trait] = max(activated_milestones)

            if not activated_traits:
                no_trait_label = QLabel("No traits activated.")
                no_trait_label.setStyleSheet("color: white;")
                traits_layout.addWidget(no_trait_label)
            else:
                for trait, highest_milestone in activated_traits.items():
                    trait_info = next((t for t in traits if t["Tộc Hệ"] == trait), None)
                    if trait_info:
                        combined_pixmap = self.parent().create_combined_icon(trait_info["Icon"][0], trait_info["Icon"][1])
                        trait_icon_label = QLabel()
                        trait_icon_label.setPixmap(combined_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        trait_name_label = QLabel(f"{trait}:")
                        trait_name_label.setStyleSheet("color: white;")
                        # Tạo layout ngang cho từng trait
                        trait_layout_item = QHBoxLayout()
                        trait_layout_item.addWidget(trait_icon_label)
                        trait_layout_item.addWidget(trait_name_label)

                        # Hiển thị các mốc đã kích hoạt
                        for milestone in traits_active.get(trait, []):
                            if milestone > highest_milestone:
                                break
                            milestone_label = QLabel(str(milestone))
                            milestone_label.setAlignment(Qt.AlignCenter)
                            milestone_label.setFixedWidth(30)
                            milestone_label.setStyleSheet(
                                """
                                QLabel {
                                    background-color: yellow;
                                    border: 1px solid black;
                                    padding: 2px;
                                    margin: 1px;
                                    border-radius: 4px;
                                    font-weight: bold;
                                }
                                """
                            )
                            trait_layout_item.addWidget(milestone_label)

                        trait_layout_item.addStretch()
                        traits_layout.addLayout(trait_layout_item)

            team_layout.addLayout(traits_layout)

            # Thêm widget vào layout
            self.scroll_layout.addWidget(team_widget)

    def delete_team(self, index):
        """Xoá đội hình tại vị trí `index`."""
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Bạn có chắc chắn muốn xoá Đội Hình {index + 1}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            success = self.team_builder_ai.delete_favorite_team(index)
            if success:
                QMessageBox.information(self, "Deleted", f"Đã xoá Đội Hình {index + 1} thành công.")
                self.populate_favorite_teams()
            else:
                QMessageBox.warning(self, "Error", "Không thể xoá đội hình.")
    
    def clear_layout(self, layout):
        """Remove all widgets from a layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

class ChampionLabel(QLabel):
    def __init__(self, champion, parent):
        super().__init__()
        self.champion = champion
        self.parent = parent
        try:
            icon_path = resource_path(self.champion["Icon"])
            self.setPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            print(f"Error loading image for {self.champion['Name']}: {e}")
            self.setText("No Image")
        self.setToolTip(self.champion["Name"])
        self.setFixedSize(70, 70)
        
        # Set border color based on cost
        border_color = self.get_border_color(self.champion["Cost"])
        self.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {border_color};
                border-radius: 5px;
            }}
        """)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

    def get_border_color(self, cost):
        if cost == 1:
            return "white"
        elif cost == 2:
            return "rgb(20, 207, 17)"
        elif cost == 3:
            return "rgb(44, 118, 233)"
        elif cost == 4:
            return "rgb(219, 31, 233)"
        elif cost == 5:
            return "rgb(184, 163, 28)"
        else:
            return "gray"

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.parent.add_champion_to_team(self.champion)
        elif event.button() == Qt.RightButton:
            self.parent.remove_champion_from_team(self.champion)

class TeamLabel(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.champion = None
        self.parent = parent
        self.setFixedSize(70, 70)
        self.setStyleSheet("border: 1px solid black;")
        self.setAlignment(Qt.AlignCenter)

    def set_champion(self, champion):
        self.champion = champion
        if champion:
            try:
                icon_path = resource_path(champion["Icon"])
                self.setPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.setToolTip(champion["Name"])
            except Exception as e:
                print(f"Error loading image for {champion['Name']}: {e}")
                self.setText("No Image")
            # Set border color based on cost
            border_color = self.get_border_color(champion["Cost"])
            self.setStyleSheet(f"""
                QLabel {{
                    border: 2px solid {border_color};
                    border-radius: 5px;
                }}
            """)

            # Add shadow effect
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(5)
            shadow.setColor(Qt.black)
            shadow.setOffset(0, 0)
            self.setGraphicsEffect(shadow)
        else:
            self.clear()
            self.setStyleSheet("border: 1px solid black; border-radius: 5px;")
            self.setToolTip("")
            self.setGraphicsEffect(None)

    def get_border_color(self, cost):
        if cost == 1:
            return "white"
        elif cost == 2:
            return "rgb(20, 207, 17)"
        elif cost == 3:
            return "rgb(44, 118, 233)"
        elif cost == 4:
            return "rgb(219, 31, 233)"
        elif cost == 5:
            return "rgb(184, 163, 28)"
        else:
            return "gray"

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton and self.champion:
            self.parent.remove_champion_from_team(self.champion)

class TeamBuilderAI:
    def __init__(self, favorites_file="favorite_teams.json"):
        self.rejected_champions = set()
        self.trait_cache = {}
        self.favorites_file = favorites_file
        self.synergy_map = self.build_synergy_map()

        # Đọc đội hình yêu thích và phân tích
        self.favorite_teams = self.load_favorite_teams()
        self.trait_preferences = self.analyze_favorite_teams()

        # Chuẩn bị dữ liệu cho KNN
        self.knn_model, self.team_vectors, self.n_neighbors = self.prepare_knn()

    def build_synergy_map(self):
        """
        Xây dựng synergy_map dựa trên dữ liệu đã cung cấp.
        """
        return {
            "Bắn Tỉa": {
                "Cỗ Máy Tự Động": 1.5,
                "Cảnh Binh": 1.3,
                "Ánh Lửa": 1.2,
                "Giám Sát": 1.2,
                "Pháo Binh": 1.1
            },
            "Chinh Phục": {
                "Vệ Binh": 2.0,
                "Song Hình": 1.5,
                "Phục Kích": 1.3,
                "Thống Trị": 1.3,
                "Võ Sĩ Lồng Sắt": 1.2,
                "Giám Sát": 1.2,
                "Tiên Tri": 1.1,
                "Sứ Giả": 1.1,
                "Phù Thủy": 1.1,
                "Tái Chế": 1.1,
                "Đấu Sĩ": 1.0
            },
            "Cảnh Binh": {
                "Phục Kích": 1.5,
                "Cực Tốc": 1.3,
                "Vệ Binh": 1.2,
                "Bắn Tỉa": 1.2,
                "Đấu Sĩ": 1.1,
                "Phù Thủy": 1.1
            },
            "Cỗ Máy Tự Động": {
                "Phục Kích": 1.5,
                "Pháo Binh": 1.3,
                "Vệ Binh": 1.2,
                "Giám Sát": 1.2,
                "Ánh Lửa": 1.2,
                "Bắn Tỉa": 1.2,
                "Thí Nghiệm": 1.1,
                "Thống Trị": 1.1,
                "Cảnh Binh": 1.1,
                "Đấu Sĩ": 1.1
            },
            "Cực Tốc": {
                "Phục Kích": 1.5,
                "Cảnh Binh": 1.3,
                "Vệ Binh": 1.2,
                "Bắn Tỉa": 1.2,
                "Đấu Sĩ": 1.1,
                "Nổi Loạn": 1.1
            },
            "Gia Đình": {
                "Phục Kích": 1.5,
                "Phù Thủy": 1.3,
                "Vệ Binh": 1.2,
                "Giám Sát": 1.2,
                "Pháo Binh": 1.1,
                "Cảnh Binh": 1.1,
                "Thống Trị": 1.1,
                "Song Hình": 1.1,
                "Tái Chế": 1.1
            },
            "Giám Sát": {
                "Vệ Binh": 2.0,
                "Phục Kích": 1.3,
                "Chinh Phục": 1.2,
                "Phù Thủy": 1.2,
                "Sứ Giả": 1.2,
                "Học Viện": 1.1,
                "Tái Chế": 1.1,
                "Cỗ Máy Tự Động": 1.1,
                "Ánh Lửa": 1.1,
                "Bắn Tỉa": 1.1,
                "Pháo Binh": 1.1,
                "Võ Sĩ Lồng Sắt": 1.1
            },
            "Hoa Hồng Đen": {
                "Phù Thủy": 1.5,
                "Sứ Giả": 1.3,
                "Chinh Phục": 1.1,
                "Vệ Binh": 1.1,
                "Song Hình": 1.1,
                "Thống Trị": 1.1,
                "Tiên Tri": 1.1
            },
            "Hóa Chủ": {
                "Phục Kích": 1.5,
                "Thí Nghiệm": 1.3,
                "Đấu Sĩ": 1.3,
                "Thống Trị": 1.2,
                "Tiên Tri": 1.2,
                "Võ Sĩ Lồng Sắt": 1.2,
                "Phù Thủy": 1.2,
                "Vệ Binh": 1.1,
                "Song Hình": 1.1,
                "Cảnh Binh": 1.1,
                "Sứ Giả": 1.1,
                "Tay Bạc": 1.1
            },
            "Học Viện": {
                "Phù Thủy": 1.5,
                "Vệ Binh": 1.3,
                "Nổi Loạn": 1.2,
                "Pháo Binh": 1.2,
                "Tái Chế": 1.2,
                "Tiên Tri": 1.1,
                "Chinh Phục": 1.1,
                "Phục Kích": 1.1
            },
            "Nổi Loạn": {
                "Vệ Binh": 2.0,
                "Phục Kích": 1.3,
                "Cảnh Binh": 1.3,
                "Tái Chế": 1.2,
                "Pháo Binh": 1.2,
                "Tiên Tri": 1.2,
                "Chinh Phục": 1.2,
                "Song Hình": 1.1,
                "Phù Thủy": 1.1,
                "Đấu Sĩ": 1.1,
                "Cực Tốc": 1.1
            },
            "Pháo Binh": {
                "Phù Thủy": 1.3,
                "Vệ Binh": 1.3,
                "Chinh Phục": 1.2,
                "Sứ Giả": 1.2,
                "Tái Chế": 1.2,
                "Cảnh Binh": 1.2,
                "Phục Kích": 1.2,
                "Cực Tốc": 1.2,
                "Đấu Sĩ": 1.1
            },
            "Phù Thủy": {
                "Hoa Hồng Đen": 1.5,
                "Phục Kích": 1.3,
                "Chinh Phục": 1.1,
                "Pháo Binh": 1.3,
                "Hóa Chủ": 1.3,
                "Tái Chế": 1.1,
                "Sứ Giả": 1.2,
                "Vệ Binh": 1.2,
                "Song Hình": 1.1
            },
            "Phục Kích": {
                "Cảnh Binh": 1.5,
                "Chinh Phục": 1.2,
                "Tái Chế": 1.5,
                "Pháo Binh": 1.2,
                "Vệ Binh": 1.2,
                "Đấu Sĩ": 1.2,
                "Phù Thủy": 1.3
            },
            "Song Hình": {
                "Chinh Phục": 1.3,
                "Võ Sĩ Lồng Sắt": 1.2,
                "Phù Thủy": 1.2,
                "Đấu Sĩ": 1.2,
                "Sứ Giả": 1.2,
                "Vệ Binh": 1.2,
                "Pháo Binh": 1.2,
                "Thống Trị": 1.2
            },
            "Sứ Giả": {
                "Chinh Phục": 1.1,
                "Vệ Binh": 1.2,
                "Song Hình": 1.2,
                "Phù Thủy": 1.2,
                "Đấu Sĩ": 1.2,
                "Thống Trị": 1.2,
                "Hóa Chủ": 1.2,
                "Cảnh Binh": 1.2,
                "Pháo Binh": 1.2
            },
            "Tay Bạc": {
                "Hóa Chủ": 1.2,
                "Võ Sĩ Lồng Sắt": 1.2
            },
            "Thí Nghiệm": {
                "Hóa Chủ": 1.3,
                "Phục Kích": 1.3,
                "Đấu Sĩ": 1.2,
                "Thống Trị": 1.2,
                "Tiên Tri": 1.2
            },
            "Thống Trị": {
                "Chinh Phục": 1.2,
                "Song Hình": 1.2,
                "Vệ Binh": 1.2,
                "Phù Thủy": 1.2,
                "Sứ Giả": 1.2,
                "Cỗ Máy Tự Động": 1.2,
                "Thí Nghiệm": 1.2,
                "Đấu Sĩ": 1.2,
                "Tiên Tri": 1.2
            },
            "Tiên Tri": {
                "Đấu Sĩ": 1.2,
                "Vệ Binh": 1.2,
                "Hóa Chủ": 1.2,
                "Phù Thủy": 1.2,
                "Tái Chế": 1.2,
                "Pháo Binh": 1.2,
                "Chinh Phục": 1.1,
                "Phục Kích": 1.2
            },
            "Tái Chế": {
                "Phục Kích": 1.5,
                "Pháo Binh": 1.3,
                "Vệ Binh": 1.2,
                "Chinh Phục": 1.1,
                "Sứ Giả": 1.2,
                "Cảnh Binh": 1.2,
                "Võ Sĩ Lồng Sắt": 1.2,
                "Phù Thủy": 1.1
            },
            "Vua Phế Liệu": {
                "Vệ Binh": 1.2,
                "Phục Kích": 1.2,
                "Chinh Phục": 1.2,
                "Song Hình": 1.2,
                "Đấu Sĩ": 1.2
            },
            "Võ Sĩ Lồng Sắt": {
                "Chinh Phục": 1.2,
                "Song Hình": 1.2,
                "Phù Thủy": 1.2,
                "Cảnh Binh": 1.2,
                "Phục Kích": 1.2,
                "Sứ Giả": 1.2,
                "Thí Nghiệm": 1.2,
                "Đấu Sĩ": 1.2,
                "Thống Trị": 1.2,
                "Vệ Binh": 1.2
            },
            "Vệ Binh": {
                "Chinh Phục": 1.2,
                "Song Hình": 1.2,
                "Phù Thủy": 1.2,
                "Pháo Binh": 1.2,
                "Tái Chế": 1.2,
                "Nổi Loạn": 1.2,
                "Thống Trị": 1.2,
                "Đấu Sĩ": 1.2,
                "Phục Kích": 1.2,
                "Cảnh Binh": 1.2,
                "Sứ Giả": 1.2,
                "Tiên Tri": 1.2
            },
            "Ánh Lửa": {
                "Pháo Binh": 1.2,
                "Cảnh Binh": 1.2,
                "Thí Nghiệm": 1.2,
                "Giám Sát": 1.2,
                "Bắn Tỉa": 1.2
            },
            "Đấu Sĩ": {
                "Phục Kích": 1.5,
                "Cảnh Binh": 1.3,
                "Sứ Giả": 1.2,
                "Thống Trị": 1.2,
                "Tiên Tri": 1.2,
                "Vệ Binh": 1.2
            }
        }

    def load_favorite_teams(self):
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"Loaded {len(data)} favorite teams.")
                    return data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {self.favorites_file}: {e}")
                return []
        print(f"{self.favorites_file} does not exist. Starting with empty favorite teams.")
        return []

    def analyze_favorite_teams(self):
        """
        Phân tích đội hình yêu thích để xác định các tộc hệ phổ biến và mối tương sinh.
        """
        trait_count = defaultdict(int)
        synergy_count = defaultdict(lambda: defaultdict(int))
        for team_entry in self.favorite_teams:
            team_traits = []
            # Tính từ các tướng trong đội
            for champ_name in team_entry["team"]:
                champ = next((c for c in champions if c["Name"] == champ_name), None)
                if champ:
                    team_traits.extend(champ["Tộc Hệ"])
            # Tính từ emblem counts
            for trait, count in team_entry["emblems"].items():
                trait_count[trait] += count
            # Tính từ các tộc hệ của các tướng
            for trait in team_traits:
                trait_count[trait] += 1

            # Tính mối tương sinh trong đội hình
            unique_traits = list(set(team_traits))
            for i in range(len(unique_traits)):
                for j in range(i + 1, len(unique_traits)):
                    trait1 = unique_traits[i]
                    trait2 = unique_traits[j]
                    if trait1 != trait2:
                        synergy_count[trait1][trait2] += 1
                        synergy_count[trait2][trait1] += 1

        # Cập nhật trait_preferences dựa trên trait_count
        self.trait_preferences = trait_count

        # Cập nhật synergy_map dựa trên synergy_count
        for trait, related_traits in synergy_count.items():
            for related_trait, count in related_traits.items():
                if trait not in self.synergy_map:
                    self.synergy_map[trait] = {}
                # Gán trọng số dựa trên tần suất
                if count >= 4:
                    weight = 1.5
                elif count >= 2:
                    weight = 1.3
                else:
                    weight = 1.1
                self.synergy_map[trait][related_trait] = weight

        return trait_count

    def prepare_knn(self):
        """
        Chuẩn bị dữ liệu cho mô hình KNN dựa trên các đội hình đã lưu.
        """
        team_vectors = []
        for team_entry in self.favorite_teams:
            vector = self.team_to_vector(team_entry)
            team_vectors.append(vector)
        
        n_samples = len(team_vectors)
        if n_samples == 0:
            print("No favorite teams to train KNN.")
            return None, None, 0  # Không có đội hình nào để fit
        else:
            # Đặt n_neighbors là tối thiểu giữa 3 và số lượng samples hiện có
            n_neighbors = n_samples
            knn = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto').fit(team_vectors)
            print(f"KNN model trained with {n_samples} teams and n_neighbors={n_neighbors}.")
            return knn, team_vectors, n_neighbors

    def team_to_vector(self, team_entry):
        """
        Chuyển đổi đội hình thành vector đặc trưng.
        """
        # Tạo một vector với chiều dài bằng số tộc hệ, mỗi phần tử đại diện cho số lượng của tộc hệ đó
        trait_list = sorted(traits_active.keys())
        vector = [0] * len(trait_list)
        trait_index = {trait: idx for idx, trait in enumerate(trait_list)}
        
        # Tính từ các tướng trong đội
        for champ_name in team_entry["team"]:
            champ = next((c for c in champions if c["Name"] == champ_name), None)
            if champ:
                for trait in champ["Tộc Hệ"]:
                    if trait in trait_index:
                        vector[trait_index[trait]] += 1
        # Tính từ emblem counts
        for trait, count in team_entry["emblems"].items():
            if trait in trait_index:
                vector[trait_index[trait]] += count
        return vector

    def find_similar_teams(self, current_team, emblem_counts, max_team_size):
        """
        Tìm các đội hình tương tự đã lưu sử dụng mô hình KNN.
        """
        if not self.knn_model or self.n_neighbors == 0:
            print("KNN model not initialized or no neighbors.")
            return []

        current_team_entry = {
            "team": [champ["Name"] for champ in current_team],
            "emblems": emblem_counts,
            "level": max_team_size
        }
        current_vector = self.team_to_vector(current_team_entry)
        
        print(f"Current Vector: {current_vector}")
        try:
            distances, indices = self.knn_model.kneighbors([current_vector])
        except Exception as e:
            print(f"Error during KNN kneighbors: {e}")
            return []

        print(f"Indices Returned by KNN: {indices}")
        print(f"Number of Favorite Teams: {len(self.favorite_teams)}")
        
        # Tránh truy cập ngoài phạm vi
        similar_teams = []
        for idx in indices[0]:
            if 0 <= idx < len(self.favorite_teams):
                similar_teams.append(self.favorite_teams[idx])
            else:
                print(f"Index {idx} is out of range for favorite_teams with length {len(self.favorite_teams)}")
        
        return similar_teams

    def _calculate_team_synergy(self, champion_traits, current_traits):
        """
        Tính toán bonus tương sinh cho tướng dựa trên synergy_map.
        """
        synergy_bonus = 0
        for trait in champion_traits:
            if trait in self.synergy_map:
                for synergy_trait, weight in self.synergy_map[trait].items():
                    if current_traits.get(synergy_trait, 0) > 0:
                        synergy_bonus += weight
        return synergy_bonus

    def _calculate_rarity_bonus(self, champion):
        """
        Tính toán bonus dựa trên độ hiếm hoặc giá tiền của tướng.
        """
        rarity_bonus_map = {
            1: 0.5,
            2: 1.0,
            3: 1.5,
            4: 2.0,
            5: 2.5
        }
        return rarity_bonus_map.get(champion["Cost"], 0)

    def _calculate_cost_penalty(self, champion):
        """
        Tính toán penalty dựa trên giá tiền của tướng để khuyến khích đội hình hiệu quả về chi phí.
        """
        cost_penalty_map = {
            1: 0,
            2: 0.2,
            3: 0.5,
            4: 0.8,
            5: 1.0
        }
        return cost_penalty_map.get(champion["Cost"], 0)

    def _calculate_champion_score(self, champion, current_traits, needed_traits, emblem_counts):
        """
        Tính toán điểm số cho từng tướng dựa trên nhiều tiêu chí.
        """
        # Tính các tộc hệ tạm thời nếu thêm tướng này
        temp_traits = current_traits.copy()
        for trait in champion["Tộc Hệ"]:
            temp_traits[trait] = temp_traits.get(trait, 0) + 1
        for trait, count in emblem_counts.items():
            temp_traits[trait] = temp_traits.get(trait, 0) + count

        # Milestone progression score
        milestone_score = 0
        for trait, milestones in traits_active.items():
            current_level = current_traits.get(trait, 0)
            new_level = temp_traits.get(trait, 0)
            
            # Tìm mốc kích hoạt tiếp theo
            next_milestone = next((m for m in milestones if m > current_level), None)
            if next_milestone:
                # Tính khoảng cách đến mốc tiếp theo trước và sau khi thêm tướng
                distance_before = next_milestone - current_level
                distance_after = next_milestone - new_level

                # Nếu khoảng cách giảm, tăng điểm
                if distance_after < distance_before:
                    milestone_score += (distance_before - distance_after) * 5  # Tăng trọng số
                # Nếu đạt được mốc mới, tăng điểm nhiều hơn
                if distance_after <= 0:
                    milestone_score += 10  # Điểm thưởng cho việc đạt mốc mới

        # Áp dụng hình phạt nếu tướng không đóng góp vào mốc kích hoạt nào
        contributes_to_milestone = any(
            temp_traits.get(trait, 0) >= milestones[0] for trait in champion["Tộc Hệ"]
        )
        if not contributes_to_milestone:
            milestone_score -= 5  # Hình phạt

        # Needed traits contribution
        needed_traits_contribution = 0
        for trait in champion["Tộc Hệ"]:
            if trait in needed_traits:
                # Tính điểm dựa trên khoảng cách đến mốc kích hoạt
                distance = needed_traits[trait]
                needed_traits_contribution += (1 / distance) * 10  # Khoảng cách càng nhỏ, điểm càng cao

        # Team diversity penalty
        team_trait_overlap = sum(
            1 for trait in champion["Tộc Hệ"] 
            if current_traits.get(trait, 0) > 0
        ) * 0.5  # Giảm trọng số

        # Synergy bonus
        synergy_bonus = self._calculate_team_synergy(champion["Tộc Hệ"], current_traits)

        # Rarity và Cost consideration
        rarity_bonus = self._calculate_rarity_bonus(champion)
        cost_penalty = self._calculate_cost_penalty(champion)

        # Preference bonus từ trait_preferences
        preference_bonus = 0
        for trait in champion["Tộc Hệ"]:
            preference_bonus += self.trait_preferences.get(trait, 0) * 0.1  # Điều chỉnh hệ số theo ý muốn

        # Trọng số cho việc hoàn thiện mốc
        milestone_completion_bonus = 0
        for trait in champion["Tộc Hệ"]:
            milestones = traits_active.get(trait, [])
            # Tìm mốc tiếp theo
            next_milestone = next((m for m in milestones if temp_traits.get(trait, 0) < m), None)
            if next_milestone:
                # Thêm điểm nếu tướng giúp đạt gần mốc tiếp theo
                distance_to_milestone = next_milestone - current_traits.get(trait, 0)
                if distance_to_milestone <= 2:
                    milestone_completion_bonus += 1.5  # Tăng trọng số

        # Tổng điểm
        score = (
            milestone_score +
            needed_traits_contribution +
            synergy_bonus +
            rarity_bonus -
            cost_penalty +
            preference_bonus
        )

        return score

    def suggest_champions(self, current_team, max_team_size, all_champions, traits_active, emblem_counts):
        """
        Đề xuất các tướng để hoàn thiện đội hình dựa trên các tiêu chí đã định.
        
        Parameters:
            current_team (list): Danh sách các tướng hiện tại trong đội.
            max_team_size (int): Kích thước tối đa của đội hình.
            all_champions (list): Danh sách tất cả các tướng có thể chọn.
            traits_active (dict): Dictionary chứa các tộc hệ và các mốc kích hoạt.
            emblem_counts (dict): Dictionary chứa số lượng emblem của mỗi tộc hệ.
        
        Returns:
            list: Danh sách các tướng được đề xuất để thêm vào đội hình.
        """
        # 1. Tính số slot còn lại
        slots_available = max_team_size - len(current_team)
        if slots_available <= 0:
            return []

        # 2. Tính các tộc hệ hiện tại từ đội hình và emblem_counts
        current_traits = defaultdict(int)
        for champ in current_team:
            for trait in champ["Tộc Hệ"]:
                current_traits[trait] += 1
        for trait, count in emblem_counts.items():
            current_traits[trait] += count

        # 3. Xác định các tộc hệ cần thiết dựa trên mốc kích hoạt
        needed_traits = {}
        for trait, milestones in traits_active.items():
            current_level = current_traits.get(trait, 0)
            # Tìm mốc kích hoạt tiếp theo
            next_milestone = next((m for m in milestones if m > current_level), None)
            if next_milestone:
                distance = next_milestone - current_level
                if distance <= slots_available + 1:  # Kiểm tra xem có thể đạt được không
                    needed_traits[trait] = distance

        # 4. Nếu không cần tộc hệ nào, sử dụng trait_preferences để đặt mục tiêu
        if not needed_traits:
            # Đặt mục tiêu dựa trên trait_preferences
            for trait, preference in self.trait_preferences.items():
                if current_traits.get(trait, 0) < preference:
                    needed_traits[trait] = preference - current_traits.get(trait, 0)

        # 5. Tìm kiếm các đội hình tương tự và điều chỉnh trait_preferences
        similar_teams = self.find_similar_teams(current_team, emblem_counts, max_team_size)
        for similar_team in similar_teams:
            for trait, count in similar_team.get("emblems", {}).items():
                self.trait_preferences[trait] += count * 0.1  # Điều chỉnh hệ số theo ý muốn
            for champ_name in similar_team.get("team", []):
                champ = next((c for c in all_champions if c["Name"] == champ_name), None)
                if champ:
                    for trait in champ["Tộc Hệ"]:
                        self.trait_preferences[trait] += 0.1  # Điều chỉnh hệ số theo ý muốn

        # 6. Lọc các tướng tiềm năng
        potential_champions = [
            champ for champ in all_champions
            if champ not in current_team
            and champ["Name"] not in self.rejected_champions
            and any(trait in needed_traits for trait in champ["Tộc Hệ"])
        ]

        if not potential_champions:
            return []

        # 7. Tính điểm số cho từng tướng tiềm năng
        champion_scores = []
        for champ in potential_champions:
            score = self._calculate_champion_score(
                champion=champ,
                current_traits=current_traits,
                needed_traits=needed_traits,
                emblem_counts=emblem_counts
            )
            champion_scores.append((champ, score))

        # 8. Sắp xếp các tướng theo điểm số giảm dần
        champion_scores.sort(key=lambda x: x[1], reverse=True)

        # 9. Sử dụng top N để chọn ngẫu nhiên, ưu tiên các tướng có điểm cao nhất
        top_n = 10  # Có thể điều chỉnh giá trị này tùy theo nhu cầu
        top_champions = champion_scores[:top_n] if len(champion_scores) >= top_n else champion_scores

        # Sử dụng random.sample để chọn ngẫu nhiên từ top_champions
        # Đảm bảo không vượt quá số slot còn lại
        num_to_select = min(len(top_champions), slots_available)
        selected_champions = random.sample(top_champions, num_to_select)

        # Lấy danh sách các tướng được chọn
        champions_to_add = [champ for champ, score in selected_champions]

        return champions_to_add

    def reject_champion(self, champion_name):
        """
        Bỏ qua một tướng để không bị đề xuất trong tương lai.
        """
        self.rejected_champions.add(champion_name)

    def clear_rejected_champions(self):
        """
        Xóa tất cả các tướng đã bị từ chối khỏi danh sách từ chối.
        """
        self.rejected_champions.clear()

    def delete_favorite_team(self, index):
        """
        Xoá đội hình yêu thích tại vị trí chỉ số `index`.
        """
        if 0 <= index < len(self.favorite_teams):
            del self.favorite_teams[index]
            self.save_favorite_teams()  # Sử dụng phương thức đúng để lưu lại danh sách
            self.analyze_favorite_teams()
            self.prepare_knn()
            print(f"Deleted favorite team at index {index}. Total favorite teams now: {len(self.favorite_teams)}")
            return True
        print(f"Failed to delete favorite team at index {index}.")
        return False

    def save_favorite_teams(self):
        """
        Ghi lại danh sách đội hình yêu thích vào file JSON.
        """
        try:
            with open(self.favorites_file, "w", encoding="utf-8") as f:
                json.dump(self.favorite_teams, f, ensure_ascii=False, indent=4)
            print(f"Saved {len(self.favorite_teams)} favorite teams to {self.favorites_file}.")
        except Exception as e:
            print(f"Error saving favorite teams: {e}")

class TFTApp(QWidget):
    def __init__(self):
        super().__init__()
        self.app_version = "v1.0.0"
        self.setWindowTitle("Siêu phẩm Flex")
        self.setGeometry(100, 100, 1400, 800)

        # Set darker background color
        self.setStyleSheet("background-color: #2F2F2F;")  # Dark gray background

        # Data Structures
        self.team = []
        self.max_team_size = 1  # Default level 1
        self.emblem_counts = {}

        self.favorites_window = None

        # Instantiate the AI module
        self.team_builder_ai = TeamBuilderAI()
        self.last_auto_added_champions = []

        self.suggested_combinations = []
        self.last_team_state = []
        self.last_auto_added_champions = []

        self.favorites_file = "favorite_teams.json"

        # Layouts
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        

        # 1. Vùng Hiển Thị Đội Hình
        self.team_layout = QHBoxLayout()
        self.team_labels = []
        for _ in range(11):  # Max team size is 11
            label = TeamLabel(self)
            self.team_layout.addWidget(label)
            self.team_labels.append(label)
        left_layout.addLayout(self.team_layout)

        # 2. Thanh Hiển Thị Tộc Hệ Kích Hoạt với Scroll Area
        traits_scroll = QScrollArea()
        traits_scroll.setWidgetResizable(True)
        traits_container = QWidget()
        self.traits_group_layout = QVBoxLayout()
        traits_container.setLayout(self.traits_group_layout)
        traits_scroll.setWidget(traits_container)
        traits_scroll.setFixedHeight(700)  # Adjust height as needed
        traits_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #2F2F2F;
                border: none;
            }
            QScrollBar:vertical {
                background: #2F2F2F;
                width: 16px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        left_layout.addWidget(traits_scroll)

        # 3. Ô Chọn Level Người Chơi
        level_layout = QHBoxLayout()
        level_label = QLabel("Level: ")
        level_label.setStyleSheet("color: white;")
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 11)
        self.level_spin.setValue(1)
        self.level_spin.valueChanged.connect(self.update_team_size)
        self.level_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3A3A3A;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 2px;
            }
        """)
        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_spin)
        level_layout.addStretch()
        left_layout.addLayout(level_layout)

        # 5. Tính Năng Sắp Xếp
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sắp xếp tướng: ")
        sort_label.setStyleSheet("color: white;")
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Sort by Cost")
        self.sort_combo.addItem("Sort by Tộc Hệ")
        self.sort_combo.addItem("All Champions")  # Added option to show all champions
        # Add all traits to the ComboBox
        sorted_traits = sorted(traits_active.keys())
        for trait in sorted_traits:
            self.sort_combo.addItem(trait)
        self.sort_combo.currentIndexChanged.connect(self.sort_champions)
        self.sort_combo.setStyleSheet("""
            QComboBox {
                background-color: #3A3A3A;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 2px;
            }
            QComboBox QAbstractItemView {
                background-color: #3A3A3A;
                selection-background-color: #555;
                color: white;
            }
        """)
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addStretch()
        left_layout.addLayout(sort_layout)

        # 6. Vùng Hiển Thị Tất Cả Các Icon Tướng
        champions_scroll = QScrollArea()
        champions_scroll.setWidgetResizable(True)
        champions_container = QWidget()
        self.champions_grid = QGridLayout()
        self.champions_grid.setSpacing(10)

        self.champions_container = champions_container
        self.populate_available_champions()

        champions_container.setLayout(self.champions_grid)
        champions_scroll.setWidget(champions_container)
        champions_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #2F2F2F;
            }
            QScrollBar:vertical {
                background: #2F2F2F;
                width: 16px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        right_layout.addWidget(QLabel("<b style='color: white;'>Champions:</b>"))
        right_layout.addWidget(champions_scroll)

        # 4. Nút Reset
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_team)
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        # Add shadow effect correctly
        reset_shadow = QGraphicsDropShadowEffect()
        reset_shadow.setBlurRadius(10)
        reset_shadow.setColor(Qt.black)
        reset_shadow.setOffset(0, 0)
        reset_button.setGraphicsEffect(reset_shadow)

        # 7. Nút Save Favorite Team
        save_button = QPushButton("Save Favorite Team")
        save_button.clicked.connect(self.save_favorite_team)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        # Add shadow effect correctly
        save_shadow = QGraphicsDropShadowEffect()
        save_shadow.setBlurRadius(10)
        save_shadow.setColor(Qt.black)
        save_shadow.setOffset(0, 0)
        save_button.setGraphicsEffect(save_shadow)

        # 8. Nút View Favorite Teams
        view_favorites_button = QPushButton("View Favorite Teams")
        view_favorites_button.clicked.connect(self.view_favorite_teams)
        view_favorites_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        # Add shadow effect correctly
        view_favorites_shadow = QGraphicsDropShadowEffect()
        view_favorites_shadow.setBlurRadius(10)
        view_favorites_shadow.setColor(Qt.black)
        view_favorites_shadow.setOffset(0, 0)
        view_favorites_button.setGraphicsEffect(view_favorites_shadow)

        # Thêm nút Auto
        auto_button = QPushButton("Auto")
        auto_button.clicked.connect(self.auto_build_team)
        # Style the button
        auto_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        # Add shadow effect correctly
        auto_shadow = QGraphicsDropShadowEffect()
        auto_shadow.setBlurRadius(10)
        auto_shadow.setColor(Qt.black)
        auto_shadow.setOffset(0, 0)
        auto_button.setGraphicsEffect(auto_shadow)

        # 12. Nút Check for Updates
        self.update_button = QPushButton("Check for Updates")
        self.update_button.clicked.connect(self.check_for_updates)
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        # Thêm hiệu ứng đổ bóng
        update_shadow = QGraphicsDropShadowEffect()
        update_shadow.setBlurRadius(10)
        update_shadow.setColor(Qt.black)
        update_shadow.setOffset(0, 0)
        self.update_button.setGraphicsEffect(update_shadow)

        # Tạo một layout ngang để chứa các nút
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(view_favorites_button)
        buttons_layout.addWidget(auto_button)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addStretch()

        # Add a stretch to push the buttons_layout to the bottom
        left_layout.addStretch()

        # Thêm các layout vào left_layout
        left_layout.addLayout(level_layout)
        left_layout.addLayout(sort_layout)
        left_layout.addLayout(buttons_layout)

        # Add layouts to main layout
        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 7)
        
        self.setLayout(main_layout)

        # Initial display updates
        self.update_team_display()
        self.update_traits_display()


    def populate_available_champions(self, sorted_champions=None, sort_by="Cost"):
        """Populate the available champions grid. If sorted_champions is provided, use it; otherwise, use the original list."""
        # Clear the existing grid
        self.clear_layout(self.champions_grid)

        if sorted_champions is None:
            sorted_champions = champions.copy()

        if sort_by == "Cost":
            # Group champions by Cost
            cost_groups = {}
            for champ in sorted_champions:
                cost = champ["Cost"]
                cost_groups.setdefault(cost, []).append(champ)

            for cost in sorted(cost_groups.keys()):
                # Add Cost label
                cost_label = QLabel(f"<b>Cost {cost}</b>")
                cost_label.setStyleSheet("font-weight: bold; color: white;")
                self.champions_grid.addWidget(cost_label, self.champions_grid.rowCount(), 0, 1, 8)
                # Add champions under this cost
                row = self.champions_grid.rowCount()
                col = 0
                for champ in cost_groups[cost]:
                    champ_label = ChampionLabel(champ, self)
                    self.champions_grid.addWidget(champ_label, row, col)
                    col += 1
                    if col >= 8:
                        col = 0
                        row += 1
                self.champions_grid.setRowStretch(row, 1)
        elif sort_by == "Sort by Tộc Hệ":
            # Group champions by Tộc Hệ
            trait_groups = {}
            for champ in sorted_champions:
                for trait in champ["Tộc Hệ"]:
                    trait_groups.setdefault(trait, []).append(champ)

            for trait in sorted(trait_groups.keys()):
                # Add Trait label
                trait_label = QLabel(f"<b>{trait}</b>")
                trait_label.setStyleSheet("font-weight: bold; color: white;")
                self.champions_grid.addWidget(trait_label, self.champions_grid.rowCount(), 0, 1, 8)
                # Add champions under this trait
                row = self.champions_grid.rowCount()
                col = 0
                for champ in trait_groups[trait]:
                    champ_label = ChampionLabel(champ, self)
                    self.champions_grid.addWidget(champ_label, row, col)
                    col += 1
                    if col >= 8:
                        col = 0
                        row += 1
                self.champions_grid.setRowStretch(row, 1)
        elif sort_by == "All Champions":
            # Display all champions without grouping
            row = 0
            col = 0
            for champ in sorted_champions:
                champ_label = ChampionLabel(champ, self)
                self.champions_grid.addWidget(champ_label, row, col)
                col += 1
                if col >= 8:
                    col = 0
                    row += 1
            self.champions_grid.setRowStretch(row, 1)
        else:
            # Assume selected_sort is a trait
            selected_trait = sort_by
            # Filter champions that have the selected trait
            trait_filtered_champions = [champ for champ in sorted_champions if selected_trait in champ["Tộc Hệ"]]
            
            if not trait_filtered_champions:
                no_trait_label = QLabel(f"No champions with trait '{selected_trait}'.")
                no_trait_label.setStyleSheet("color: white;")
                self.champions_grid.addWidget(no_trait_label, 0, 0)
                return

            # Group the filtered champions by Cost or another criteria if needed
            cost_groups = {}
            for champ in trait_filtered_champions:
                cost = champ["Cost"]
                cost_groups.setdefault(cost, []).append(champ)

            for cost in sorted(cost_groups.keys()):
                # Add Cost label
                cost_label = QLabel(f"<b>Cost {cost}</b>")
                cost_label.setStyleSheet("font-weight: bold; color: white;")
                self.champions_grid.addWidget(cost_label, self.champions_grid.rowCount(), 0, 1, 8)
                # Add champions under this cost
                row = self.champions_grid.rowCount()
                col = 0
                for champ in cost_groups[cost]:
                    champ_label = ChampionLabel(champ, self)
                    self.champions_grid.addWidget(champ_label, row, col)
                    col += 1
                    if col >= 8:
                        col = 0
                        row += 1
                self.champions_grid.setRowStretch(row, 1)

    def create_combined_icon(self, base_path, overlay_path):
        base_pixmap = QPixmap(resource_path(base_path))
        overlay_pixmap = QPixmap(resource_path(overlay_path))

        # Điều chỉnh kích thước overlay dựa trên tên file
        if os.path.basename(overlay_path).lower() == "invoker.png":
            # Scale invoker.png thành 40x40 để vừa vào base.png (52x58)
            overlay_pixmap = overlay_pixmap.scaled(29, 29, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            # Các icon khác được scale về 32x32
            overlay_pixmap = overlay_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        combined = QPixmap(base_pixmap.size())
        combined.fill(Qt.transparent)

        painter = QPainter(combined)
        painter.drawPixmap(0, 0, base_pixmap)

        # Tính toán vị trí để overlay nằm chính giữa base
        x = (base_pixmap.width() - overlay_pixmap.width()) // 2
        y = (base_pixmap.height() - overlay_pixmap.height()) // 2
        painter.drawPixmap(x, y, overlay_pixmap)
        painter.end()

        return combined

    def update_traits_display(self):
        # Clear the previous trait display
        self.clear_layout(self.traits_group_layout)

        # Calculate current traits from champions
        current_traits = {}
        for champ in self.team:
            for trait in champ["Tộc Hệ"]:
                current_traits[trait] = current_traits.get(trait, 0) + 1

        # Add Emblem counts to current_traits
        for trait, count in self.emblem_counts.items():
            current_traits[trait] = current_traits.get(trait, 0) + count

        if not current_traits:
            return  # No traits to display

        # Build the traits display dynamically
        header_label = QLabel("<b>Tộc Hệ Activated:</b>")
        header_label.setStyleSheet("color: white;")
        self.traits_group_layout.addWidget(header_label)

        for trait in sorted(current_traits.keys()):
            h_layout = QHBoxLayout()
            
            # Tìm trait trong danh sách traits để lấy icon
            trait_info = next((t for t in traits if t["Tộc Hệ"] == trait), None)
            if trait_info:
                combined_pixmap = self.create_combined_icon(trait_info["Icon"][0], trait_info["Icon"][1])
                icon_label = QLabel()
                icon_label.setPixmap(combined_pixmap.scaled(52, 58, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                h_layout.addWidget(icon_label)
            else:
                # Nếu không tìm thấy icon, thêm một khoảng trống
                spacer = QLabel()
                spacer.setFixedWidth(52)
                spacer.setFixedHeight(58)
                h_layout.addWidget(spacer)

            trait_label = QLabel(f"{trait}: ")
            trait_label.setFixedWidth(100)
            trait_label.setStyleSheet("color: white;")
            h_layout.addWidget(trait_label)

            # Add '-' button
            minus_button = QPushButton('-')
            minus_button.setFixedWidth(25)
            minus_button.setFixedHeight(25)
            minus_button.clicked.connect(lambda checked, t=trait: self.remove_emblem(t))
            h_layout.addWidget(minus_button)

            # Show Emblem count (if any)
            emblem_count = self.emblem_counts.get(trait, 0)
            emblem_count_label = QLabel(f"{emblem_count}")
            emblem_count_label.setFixedWidth(20)
            emblem_count_label.setAlignment(Qt.AlignCenter)
            emblem_count_label.setStyleSheet("color: white;")
            h_layout.addWidget(emblem_count_label)

            # Add '+' button
            plus_button = QPushButton('+')
            plus_button.setFixedWidth(25)
            plus_button.setFixedHeight(25)
            plus_button.clicked.connect(lambda checked, t=trait: self.add_emblem(t))
            h_layout.addWidget(plus_button)

            numbers = traits_active.get(trait, [])
            count = current_traits[trait]

            # Determine if the trait is activated
            activated = False
            for num in numbers:
                num_label = QLabel(str(num))
                num_label.setAlignment(Qt.AlignCenter)
                num_label.setFixedWidth(30)
                if count >= num:
                    # Trait is activated at this threshold
                    num_label.setStyleSheet(
                        """
                        QLabel {
                            background-color: yellow;
                            border: 1px solid black;
                            padding: 2px;
                            margin: 1px;
                            border-radius: 4px;
                            font-weight: bold;
                        }
                        """
                    )
                    activated = True
                else:
                    # Trait not activated at this threshold
                    num_label.setStyleSheet(
                        """
                        QLabel {
                            background-color: lightgray;
                            border: 1px solid black;
                            padding: 2px;
                            margin: 1px;
                            border-radius: 4px;
                        }
                        """
                    )
                h_layout.addWidget(num_label)

            h_layout.addStretch()
            if activated:
                # Highlight the trait label if activated
                trait_label.setStyleSheet("font-weight: bold; color: green;")
            else:
                trait_label.setStyleSheet("color: white;")
            self.traits_group_layout.addLayout(h_layout)

    def add_emblem(self, trait):
        self.emblem_counts[trait] = self.emblem_counts.get(trait, 0) + 1
        self.update_traits_display()

    def remove_emblem(self, trait):
        if trait in self.emblem_counts and self.emblem_counts[trait] > 0:
            self.emblem_counts[trait] -= 1
            if self.emblem_counts[trait] == 0:
                del self.emblem_counts[trait]
        self.update_traits_display()

    def clear_layout(self, layout):
        """Remove all widgets from a layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def sort_champions(self):
        """Sort the champions based on the selected criteria and repopulate the grid."""
        selected_sort = self.sort_combo.currentText()
        if selected_sort == "Sort by Cost":
            sorted_champions = sorted(champions, key=lambda x: x["Cost"])
            self.populate_available_champions(sorted_champions, sort_by="Cost")
        elif selected_sort == "Sort by Tộc Hệ":
            sorted_champions = sorted(champions, key=lambda x: x["Name"])  # Sort alphabetically by name within traits
            self.populate_available_champions(sorted_champions, sort_by="Sort by Tộc Hệ")
        elif selected_sort == "All Champions":
            sorted_champions = sorted(champions, key=lambda x: x["Name"])
            self.populate_available_champions(sorted_champions, sort_by="All Champions")
        else:
            # Assume selected_sort is a trait
            selected_trait = selected_sort
            self.populate_available_champions(sort_by=selected_trait)

    def auto_build_team(self):
        champions_to_add = self.team_builder_ai.suggest_champions(
            current_team=self.team,
            max_team_size=self.max_team_size,
            all_champions=champions,
            traits_active=traits_active,
            emblem_counts=self.emblem_counts
        )

        if not champions_to_add:
            QMessageBox.information(self, "Auto Build", "Không tìm thấy tướng phù hợp để thêm.")
            return

        self.team.extend(champions_to_add)
        self.update_team_display()
        self.update_traits_display()
        # Keep track of last auto-added champions
        self.last_auto_added_champions = champions_to_add.copy()

    def add_champion_to_team(self, champion):
        if len(self.team) >= self.max_team_size:
            QMessageBox.warning(self, "Team Full", f"Bạn chỉ có thể có tối đa {self.max_team_size} tướng trên sân.")
            return
        if champion in self.team:
            QMessageBox.information(self, "Already in Team", f"{champion['Name']} đã có trong đội hình.")
            return

        self.team.append(champion)
        self.update_team_display()
        self.update_traits_display()

        # Reset AI rejected champions if the team changes manually
        self.team_builder_ai.rejected_champions.clear()
        self.last_auto_added_champions = []

    def remove_champion_from_team(self, champion):
        if champion in self.team:
            self.team.remove(champion)
            self.update_team_display()
            self.update_traits_display()
            if champion in self.last_auto_added_champions:
                self.last_auto_added_champions.remove(champion)
                # Inform the AI that the champion was rejected
                self.team_builder_ai.rejected_champions.add(champion["Name"])
        else:
            QMessageBox.information(self, "Not in Team", f"{champion['Name']} không có trong đội hình.")

    def reset_team(self):
        self.team = []
        self.emblem_counts = {}  # Reset Emblem counts
        self.update_team_display()
        self.update_traits_display()
        self.suggested_combinations = []
        self.last_team_state = []
        self.last_auto_added_champions = []

    def update_team_display(self):
        for i, label in enumerate(self.team_labels):
            if i < len(self.team):
                champ = self.team[i]
                label.set_champion(champ)
            else:
                label.set_champion(None)

    def update_team_size(self):
        self.max_team_size = self.level_spin.value()
        # Nếu đội hình hiện tại vượt quá kích thước mới, cắt bỏ các tướng vượt
        if len(self.team) > self.max_team_size:
            self.team = self.team[:self.max_team_size]
            self.update_team_display()
            self.update_traits_display()

    def save_favorite_team(self):
        if not self.team:
            QMessageBox.warning(self, "No Team", "Bạn chưa chọn đội hình nào để lưu.")
            return

        # Tạo một danh sách chứa tên các tướng trong đội
        team_names = [champ["Name"] for champ in self.team]
        print(f"Saving team: {team_names}")  # Debug

        # Kiểm tra xem file đã tồn tại chưa
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, "r", encoding="utf-8") as f:
                    favorite_teams = json.load(f)
                    print(f"Loaded {len(favorite_teams)} favorite teams from JSON.")  # Debug
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {self.favorites_file}: {e}")
                favorite_teams = []
        else:
            favorite_teams = []
            print(f"{self.favorites_file} does not exist. Starting with empty favorite teams.")  # Debug

        # Thêm đội hình mới vào danh sách
        favorite_teams.append({
            "team": team_names,
            "emblems": self.emblem_counts.copy(),
            "level": self.max_team_size
        })
        print(f"Appended new team. Total favorite teams now: {len(favorite_teams)}")  # Debug

        # Ghi lại vào file
        with open(self.favorites_file, "w", encoding="utf-8") as f:
            json.dump(favorite_teams, f, ensure_ascii=False, indent=4)
        print(f"Saved favorite teams to {self.favorites_file}.")  # Debug

        # Cập nhật lại dữ liệu trong AI
        self.team_builder_ai.favorite_teams = favorite_teams
        self.team_builder_ai.analyze_favorite_teams()
        self.team_builder_ai.prepare_knn()
        print("Updated TeamBuilderAI with new favorite teams.")  # Debug

        # Làm mới cửa sổ FavoriteTeamsWindow nếu đang mở
        if self.favorites_window and self.favorites_window.isVisible():
            self.favorites_window.populate_favorite_teams()
            print("Refreshed FavoriteTeamsWindow.")

        QMessageBox.information(self, "Saved", "Đội hình đã được lưu thành công!")

    def view_favorite_teams(self):
        """Mở cửa sổ FavoriteTeamsWindow để xem và xoá đội hình yêu thích."""
        if self.favorites_window is None or not self.favorites_window.isVisible():
            self.favorites_window = FavoriteTeamsWindow(self.team_builder_ai, self)
            self.favorites_window.exec_()
        else:
            self.favorites_window.populate_favorite_teams()

    def check_for_update():
        try:
            response = requests.get("https://raw.githubusercontent.com/jerrylemin/FLEXTFT/main/version.json")
            if response.status_code == 200:
                latest_version = response.json()
                current_version = "1.0.0"  # Phiên bản hiện tại
                if current_version < latest_version["version"]:
                    download_url = latest_version["url"]
                    changelog = latest_version.get("changelog", "Không có ghi chú.")
                    reply = QMessageBox.question(
                        None,
                        "Cập Nhật Mới",
                        f"Có phiên bản mới: {latest_version['version']}\n\nGhi chú: {changelog}\n\nBạn có muốn cập nhật ngay?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.Yes:
                        download_and_replace(download_url)
                else:
                    QMessageBox.information(None, "Kiểm Tra Cập Nhật", "Bạn đang sử dụng phiên bản mới nhất.")
            else:
                QMessageBox.warning(None, "Lỗi", "Không thể kiểm tra bản cập nhật.")
        except Exception as e:
            QMessageBox.warning(None, "Lỗi", f"Đã xảy ra lỗi: {e}")

    def download_and_replace(url):
        try:
            new_file_path = os.path.join(os.getcwd(), "SieuPhamFlex_new.exe")
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(new_file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            QMessageBox.information(None, "Tải Về Thành Công", "Tệp cập nhật đã được tải về.\nỨng dụng sẽ khởi động lại để áp dụng cập nhật.")
            restart_with_new_version(new_file_path)
        except Exception as e:
            QMessageBox.warning(None, "Lỗi", f"Không thể tải bản cập nhật: {e}")

    def restart_with_new_version(new_file_path):
        try:
            old_file_path = sys.argv[0]
            os.rename(old_file_path, old_file_path + ".old")
            os.rename(new_file_path, old_file_path)
            QMessageBox.information(None, "Cập Nhật", "Cập nhật thành công! Ứng dụng sẽ khởi động lại.")
            os.execl(old_file_path, old_file_path, *sys.argv)
        except Exception as e:
            QMessageBox.warning(None, "Lỗi", f"Không thể áp dụng bản cập nhật: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TFTApp()
    window.show()
    sys.exit(app.exec_())
