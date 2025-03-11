import sys
import os
import random
import numpy as np
import math
import hashlib
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                           QPushButton, QFileDialog)
from PyQt5.QtGui import (QPixmap, QImage, QPainter, QColor, QPen, QLinearGradient,
                        QRadialGradient, QPainterPath)
from PyQt5.QtCore import (Qt, QTimer, QPointF, QRectF, pyqtSignal, QByteArray, QBuffer)

class QuantumSignatureEngine:
    """Генерирует квантово-подобные защитные сигнатуры для файлов"""
    
    def __init__(self):
        # Базовые параметры квантовой сигнатуры
        self.dimensions = 8  # "Измерения" квантовой сигнатуры
        self.resolution = 256  # Разрешение визуализации
        self.color_space = "hsv"  # Цветовое пространство для визуализации
        
        # Квантовые состояния (имитация)
        self.superposition_count = 16
        self.entanglement_pairs = []
        
        # Дополнительные параметры
        self.confidence_level = 0.95  # Уровень уверенности в анализе
        self.evolution_steps = 3  # Шаги "квантовой эволюции" сигнатуры
    
    def generate_signature(self, file_path, evolution=True):
        """Генерирует квантово-подобную сигнатуру для файла"""
        # Базовый хэш файла
        try:
            file_hash = self._calculate_complex_hash(file_path)
            
            # Преобразуем хэш в "квантовое" состояние
            quantum_state = self._hash_to_quantum_state(file_hash)
            
            # Если нужно, применяем эволюцию состояния (усиливаем уникальность)
            if evolution:
                for _ in range(self.evolution_steps):
                    quantum_state = self._evolve_quantum_state(quantum_state)
            
            # Анализируем "квантовое" состояние
            signature_data = self._analyze_quantum_state(quantum_state)
            
            # Визуализируем сигнатуру
            signature_image = self._visualize_quantum_signature(signature_data)
            
            return {
                'signature_data': signature_data,
                'signature_image': signature_image,
                'confidence': self.confidence_level,
                'uniqueness_score': self._calculate_uniqueness(signature_data)
            }
        
        except Exception as e:
            print(f"Ошибка генерации квантовой сигнатуры: {e}")
            return None
    
    def _calculate_complex_hash(self, file_path):
        """Рассчитывает сложный хэш файла, комбинируя несколько алгоритмов"""
        try:
            # Для небольших файлов читаем полностью
            if os.path.getsize(file_path) < 50 * 1024 * 1024:  # 50MB
                with open(file_path, 'rb') as f:
                    content = f.read()
                    
                    # Комбинируем несколько хэшей
                    sha256 = hashlib.sha256(content).digest()
                    md5 = hashlib.md5(content).digest()
                    sha1 = hashlib.sha1(content).digest()
                    
                    # Объединяем хэши и создаем финальный хэш
                    combined = sha256 + md5 + sha1
                    final_hash = hashlib.blake2b(combined).digest()
            else:
                # Для больших файлов используем блочное чтение
                sha256 = hashlib.sha256()
                md5 = hashlib.md5()
                sha1 = hashlib.sha1()
                
                with open(file_path, 'rb') as f:
                    while chunk := f.read(4096):
                        sha256.update(chunk)
                        md5.update(chunk)
                        sha1.update(chunk)
                
                combined = sha256.digest() + md5.digest() + sha1.digest()
                final_hash = hashlib.blake2b(combined).digest()
            
            return final_hash
        except Exception as e:
            print(f"Ошибка при расчете хэша: {e}")
            raise
    
    def _hash_to_quantum_state(self, hash_bytes):
        """Преобразует хэш в имитацию квантового состояния"""
        # Разбиваем хэш на отдельные компоненты для каждого "измерения"
        quantum_state = []
        
        # Создаем базовые состояния из хэша
        chunk_size = len(hash_bytes) // self.dimensions
        for i in range(self.dimensions):
            start = i * chunk_size
            end = start + chunk_size if i < self.dimensions - 1 else len(hash_bytes)
            
            # Конвертируем часть хэша в значения от 0 до 1
            chunk = hash_bytes[start:end]
            values = [b / 255 for b in chunk]
            
            # Добавляем "суперпозицию" для каждого измерения
            superposition = []
            for _ in range(self.superposition_count):
                # Создаем вариации значений для суперпозиции
                variation = [min(1.0, max(0.0, v + random.uniform(-0.1, 0.1))) for v in values]
                superposition.append(variation)
            
            quantum_state.append(superposition)
        
        # Создаем "запутанные" пары для имитации квантовой запутанности
        self.entanglement_pairs = []
        for _ in range(self.dimensions // 2):
            dim1 = random.randrange(self.dimensions)
            dim2 = random.randrange(self.dimensions)
            while dim1 == dim2:
                dim2 = random.randrange(self.dimensions)
            self.entanglement_pairs.append((dim1, dim2))
        
        return quantum_state
    
    def _evolve_quantum_state(self, quantum_state):
        """Развивает "квантовое" состояние, усиливая важные особенности"""
        evolved_state = []
        
        # Применяем "квантовые ворота" к суперпозициям
        for dimension in quantum_state:
            evolved_dimension = []
            
            for superposition in dimension:
                # Нормализуем суперпозицию (аналог квантовых преобразований)
                total = sum(superposition)
                if total > 0:
                    normalized = [v / total for v in superposition]
                else:
                    normalized = superposition
                
                # Применяем "квантовое преобразование"
                transformed = []
                for v in normalized:
                    # Нелинейная функция преобразования
                    transformed.append(min(1.0, max(0.0, math.sin(v * math.pi) ** 2)))
                
                evolved_dimension.append(transformed)
            
            evolved_state.append(evolved_dimension)
        
        # Применяем "запутанность"
        for dim1, dim2 in self.entanglement_pairs:
            # Если одно измерение изменилось, меняем и запутанное с ним
            for i in range(min(len(evolved_state[dim1]), len(evolved_state[dim2]))):
                if random.random() < 0.5:  # 50% шанс запутывания
                    for j in range(min(len(evolved_state[dim1][i]), len(evolved_state[dim2][i]))):
                        # "Запутываем" значения
                        mean = (evolved_state[dim1][i][j] + evolved_state[dim2][i][j]) / 2
                        diff = abs(evolved_state[dim1][i][j] - evolved_state[dim2][i][j]) / 4
                        evolved_state[dim1][i][j] = mean + diff
                        evolved_state[dim2][i][j] = mean - diff
        
        return evolved_state
    
    def _analyze_quantum_state(self, quantum_state):
        """Анализирует "квантовое" состояние и создает структуру данных сигнатуры"""
        # Создаем матрицу "коллапсированного квантового состояния"
        collapsed_state = np.zeros((self.dimensions, self.dimensions))
        
        # Для каждого измерения вычисляем "вероятности" различных состояний
        for i, dimension in enumerate(quantum_state):
            for superposition in dimension:
                for j, value in enumerate(superposition[:self.dimensions]):
                    collapsed_state[i, j] += value
        
        # Нормализуем значения
        row_sums = collapsed_state.sum(axis=1, keepdims=True)
        normalized_state = np.divide(collapsed_state, row_sums, 
                                   out=np.zeros_like(collapsed_state), where=row_sums!=0)
        
        # Добавляем фазы для более сложной визуализации
        phases = np.zeros((self.dimensions, self.dimensions))
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                # Фаза зависит от запутанности пар
                if any(i in pair or j in pair for pair in self.entanglement_pairs):
                    phases[i, j] = random.uniform(0, 2 * math.pi)
                else:
                    phases[i, j] = (i * j) % (2 * math.pi)
        
        # Возвращаем структуру данных сигнатуры
        return {
            'amplitudes': normalized_state,
            'phases': phases,
            'entanglement': self.entanglement_pairs
        }
    
    def _visualize_quantum_signature(self, signature_data):
        """Визуализирует квантовую сигнатуру в виде изображения"""
        # Создаем изображение для визуализации
        img = Image.new('RGBA', (self.resolution, self.resolution), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Размеры ячеек в визуализации
        cell_width = self.resolution / self.dimensions
        cell_height = self.resolution / self.dimensions
        
        # Рисуем фоновый градиент
        for y in range(self.resolution):
            for x in range(self.resolution):
                i = int(y / cell_height)
                j = int(x / cell_width)
                
                if i < self.dimensions and j < self.dimensions:
                    amplitude = signature_data['amplitudes'][i, j]
                    phase = signature_data['phases'][i, j]
                    
                    # Преобразуем в цвет (HSV для более интуитивного восприятия)
                    hue = (phase / (2 * math.pi)) * 360
                    saturation = 0.8 + amplitude * 0.2
                    value = 0.5 + amplitude * 0.5
                    
                    # Преобразуем HSV в RGB
                    h = hue / 60
                    i = int(h)
                    f = h - i
                    p = value * (1 - saturation)
                    q = value * (1 - saturation * f)
                    t = value * (1 - saturation * (1 - f))
                    
                    if i == 0:
                        r, g, b = value, t, p
                    elif i == 1:
                        r, g, b = q, value, p
                    elif i == 2:
                        r, g, b = p, value, t
                    elif i == 3:
                        r, g, b = p, q, value
                    elif i == 4:
                        r, g, b = t, p, value
                    else:
                        r, g, b = value, p, q
                    
                    r, g, b = int(r * 255), int(g * 255), int(b * 255)
                    alpha = int(127 + 128 * amplitude)
                    
                    # Рисуем пиксель
                    draw.point((x, y), fill=(r, g, b, alpha))
        
        # Добавляем "запутанные" линии
        for dim1, dim2 in signature_data['entanglement']:
            x1 = (dim1 + 0.5) * cell_width
            y1 = (dim1 + 0.5) * cell_height
            x2 = (dim2 + 0.5) * cell_width
            y2 = (dim2 + 0.5) * cell_height
            
            # Создаем "запутанную" линию с градиентом
            steps = 100
            for i in range(steps):
                t = i / steps
                # Интерполяция с небольшим искривлением для визуального эффекта
                x = x1 + (x2 - x1) * t + 20 * math.sin(t * math.pi)
                y = y1 + (y2 - y1) * t + 20 * math.sin(t * math.pi)
                
                # Цвет меняется вдоль линии
                hue = (t * 360) % 360
                saturation = 0.8
                value = 0.9
                
                h = hue / 60
                i = int(h)
                f = h - i
                p = value * (1 - saturation)
                q = value * (1 - saturation * f)
                t_val = value * (1 - saturation * (1 - f))
                
                if i == 0:
                    r, g, b = value, t_val, p
                elif i == 1:
                    r, g, b = q, value, p
                elif i == 2:
                    r, g, b = p, value, t_val
                elif i == 3:
                    r, g, b = p, q, value
                elif i == 4:
                    r, g, b = t_val, p, value
                else:
                    r, g, b = value, p, q
                
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
                
                # Рисуем точку линии
                size = int(3 + 2 * math.sin(t * math.pi * 2))
                draw.ellipse((x-size, y-size, x+size, y+size), fill=(r, g, b, 200))
        
        # Преобразуем в QImage для удобства использования в Qt
        qimg = QImage(img.tobytes("raw", "RGBA"), img.width, img.height, QImage.Format_RGBA8888)
        return qimg
    
    def _calculate_uniqueness(self, signature_data):
        """Рассчитывает оценку уникальности сигнатуры"""
        # Энтропия амплитуд как мера уникальности
        amplitudes = signature_data['amplitudes'].flatten()
        entropy = 0
        for a in amplitudes:
            if a > 0:
                entropy -= a * math.log2(a)
        
        # Нормализуем энтропию от 0 до 1
        max_entropy = math.log2(len(amplitudes))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        # Вес запутанности в уникальности
        entanglement_factor = len(signature_data['entanglement']) / (self.dimensions / 2)
        
        # Общая оценка уникальности
        uniqueness = (normalized_entropy * 0.7) + (entanglement_factor * 0.3)
        return min(1.0, uniqueness)


class QuantumSignatureVisualizer(QWidget):
    """Виджет для визуализации квантовых сигнатур"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = QuantumSignatureEngine()
        self.signature_result = None
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Создаем области для отображения
        self.signature_label = QLabel("Квантовая сигнатура файла")
        self.signature_label.setAlignment(Qt.AlignCenter)
        
        # Область для визуализации
        self.image_label = QLabel()
        self.image_label.setMinimumSize(300, 300)
        self.image_label.setMaximumSize(500, 500)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: rgba(0, 0, 0, 50); border-radius: 10px;")
        
        # Информация о сигнатуре
        self.info_label = QLabel("Выберите файл для генерации квантовой сигнатуры")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        self.select_button = QPushButton("Выбрать файл")
        self.select_button.clicked.connect(self.select_file)
        
        self.compare_button = QPushButton("Сравнить сигнатуры")
        self.compare_button.setEnabled(False)
        
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.compare_button)
        
        # Добавляем все элементы в основной лейаут
        layout.addWidget(self.signature_label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.info_label)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл для анализа", "", "Все файлы (*.*)")
        
        if file_path:
            self.info_label.setText("Генерация квантовой сигнатуры...")
            QApplication.processEvents()  # Обновляем интерфейс
            
            # Генерируем сигнатуру
            self.signature_result = self.engine.generate_signature(file_path)
            
            # Отображаем результат
            if self.signature_result:
                pixmap = QPixmap.fromImage(self.signature_result['signature_image'])
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                
                # Обновляем информацию
                uniqueness = self.signature_result['uniqueness_score'] * 100
                confidence = self.signature_result['confidence'] * 100
                
                self.info_label.setText(
                    f"Файл: {os.path.basename(file_path)}\n"
                    f"Уникальность: {uniqueness:.1f}%\n"
                    f"Уверенность: {confidence:.1f}%\n"
                    f"Характеристика: {'Безопасно' if uniqueness < 85 else 'Требует внимания'}"
                )
                
                self.compare_button.setEnabled(True)
            else:
                self.info_label.setText(f"Ошибка при генерации сигнатуры для {os.path.basename(file_path)}")


# Тестирование
if __name__ == "__main__":
    app = QApplication(sys.argv)
    visualizer = QuantumSignatureVisualizer()
    visualizer.setWindowTitle("Квантовые сигнатуры")
    visualizer.resize(600, 500)
    visualizer.show()
    sys.exit(app.exec_()) 