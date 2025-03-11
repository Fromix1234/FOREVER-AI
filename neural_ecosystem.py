import sys
import os
import time
import math
import random
import logging
import psutil
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout)
from PyQt5.QtGui import (QColor, QPainter, QLinearGradient, QPen, QRadialGradient,
                        QPainterPath, QFont)
from PyQt5.QtCore import (Qt, QTimer, QPointF, QRectF)

class NeuralEcosystemMap(QWidget):
    """Визуализирует компьютерную систему как живую нейронную сеть"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        
        # Системные узлы (процессы, файлы, соединения)
        self.nodes = []
        # Соединения между узлами
        self.connections = []
        # Аномальные активности
        self.anomalies = []
        
        # Параметры визуализации
        self.zoom_level = 1.0
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.is_panning = False
        self.last_mouse_pos = None
        
        # Анимация
        self.pulse_factor = 0
        self.energy_flow = 0
        
        # Таймеры для анимации
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(30)
        
        # Таймер для обновления данных
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_system_data)
        self.update_timer.start(2000)  # Обновляем каждые 2 секунды
        
        # Загружаем начальные данные
        self.update_system_data()
        
        # Включаем отслеживание мыши
        self.setMouseTracking(True)
    
    def update_animation(self):
        """Обновляет анимацию нейронной сети"""
        self.pulse_factor = 0.5 + 0.5 * math.sin(time.time() * 2)
        self.energy_flow = (self.energy_flow + 0.05) % 1.0
        
        # Обновляем положение узлов (симуляция движения нейронов)
        for node in self.nodes:
            # Добавляем небольшое случайное движение
            node['x'] += random.uniform(-0.5, 0.5)
            node['y'] += random.uniform(-0.5, 0.5)
            
            # Ограничиваем движение в пределах разумной области
            node['x'] = max(50, min(self.width() - 50, node['x']))
            node['y'] = max(50, min(self.height() - 50, node['y']))
        
        # Обновляем состояние аномалий
        for anomaly in self.anomalies:
            anomaly['intensity'] = min(1.0, anomaly['intensity'] + random.uniform(-0.1, 0.15))
            if anomaly['intensity'] <= 0:
                self.anomalies.remove(anomaly)
        
        self.update()  # Запрашиваем перерисовку
    
    def update_system_data(self):
        """Обновляет данные о системных процессах и соединениях"""
        try:
            # Получаем информацию о процессах
            processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
            
            # Очищаем предыдущие данные, сохраняя позиции существующих узлов
            existing_positions = {node['id']: (node['x'], node['y']) for node in self.nodes}
            self.nodes.clear()
            self.connections.clear()
            
            # Ограничиваем количество отображаемых процессов для производительности
            top_processes = sorted(processes, key=lambda p: p.info['cpu_percent'] + p.info['memory_percent'], 
                                reverse=True)[:30]
            
            # Добавляем узлы для процессов
            for process in top_processes:
                node_id = f"proc_{process.info['pid']}"
                
                # Если узел существовал ранее, используем его координаты
                if node_id in existing_positions:
                    x, y = existing_positions[node_id]
                else:
                    # Иначе размещаем в случайном месте
                    x = random.uniform(100, self.width() - 100)
                    y = random.uniform(100, self.height() - 100)
                
                self.nodes.append({
                    'id': node_id,
                    'type': 'process',
                    'name': process.info['name'],
                    'activity': process.info['cpu_percent'] / 100,
                    'size': 10 + process.info['memory_percent'] * 2,
                    'x': x,
                    'y': y,
                    'color': QColor(88, 180, 255) if process.info['cpu_percent'] < 10 else QColor(255, 180, 0)
                })
            
            # Создаем связи между процессами (на основе предполагаемых взаимодействий)
            for i, node1 in enumerate(self.nodes):
                # Соединяем с несколькими ближайшими узлами
                nodes_by_distance = sorted(self.nodes[:i] + self.nodes[i+1:], 
                                         key=lambda n: ((n['x'] - node1['x'])**2 + (n['y'] - node1['y'])**2))
                
                for node2 in nodes_by_distance[:3]:  # Соединяем с 3 ближайшими
                    self.connections.append({
                        'source': node1['id'],
                        'target': node2['id'],
                        'strength': random.uniform(0.1, 1.0)
                    })
            
            # Периодически добавляем "аномалии" для интерактивности
            if random.random() < 0.1:  # 10% шанс на каждое обновление
                random_node = random.choice(self.nodes)
                self.anomalies.append({
                    'x': random_node['x'],
                    'y': random_node['y'],
                    'radius': 0,
                    'max_radius': 100,
                    'intensity': 1.0,
                    'color': QColor(255, 80, 80) if random.random() < 0.3 else QColor(255, 180, 0)
                })
        
        except Exception as e:
            logging.error(f"Ошибка при обновлении данных экосистемы: {e}")
    
    def paintEvent(self, event):
        """Отрисовка нейронной карты экосистемы"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Применяем текущий масштаб и сдвиг
        painter.translate(self.pan_offset_x, self.pan_offset_y)
        painter.scale(self.zoom_level, self.zoom_level)
        
        # Рисуем соединения между узлами
        for connection in self.connections:
            source = next((n for n in self.nodes if n['id'] == connection['source']), None)
            target = next((n for n in self.nodes if n['id'] == connection['target']), None)
            
            if source and target:
                # Рассчитываем начальную и конечную точки
                start_x, start_y = source['x'], source['y']
                end_x, end_y = target['x'], target['y']
                
                # Создаем градиент для соединения
                gradient = QLinearGradient(start_x, start_y, end_x, end_y)
                
                # Цвет и толщина зависят от силы связи
                connection_color = QColor(180, 180, 255, int(150 * connection['strength']))
                
                # Анимируем поток энергии по соединениям
                gradient.setColorAt(0, connection_color)
                gradient.setColorAt(self.energy_flow, QColor(255, 255, 255, 200))
                gradient.setColorAt(min(self.energy_flow + 0.1, 1.0), connection_color)
                gradient.setColorAt(1, connection_color)
                
                painter.setPen(QPen(gradient, 1 + 2 * connection['strength']))
                painter.drawLine(start_x, start_y, end_x, end_y)
        
        # Рисуем аномалии (круги распространения)
        for anomaly in self.anomalies:
            # Увеличиваем радиус для анимации распространения
            anomaly['radius'] = min(anomaly['radius'] + 2, anomaly['max_radius'])
            
            # Рисуем пульсирующий круг
            gradient = QRadialGradient(anomaly['x'], anomaly['y'], anomaly['radius'])
            anomaly_color = anomaly['color']
            
            # Прозрачность зависит от интенсивности
            alpha = int(100 * anomaly['intensity'])
            gradient.setColorAt(0, QColor(anomaly_color.red(), anomaly_color.green(), 
                                        anomaly_color.blue(), alpha))
            gradient.setColorAt(0.7, QColor(anomaly_color.red(), anomaly_color.green(), 
                                          anomaly_color.blue(), alpha // 2))
            gradient.setColorAt(1, QColor(anomaly_color.red(), anomaly_color.green(), 
                                        anomaly_color.blue(), 0))
            
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(anomaly['x'], anomaly['y']), 
                              anomaly['radius'], anomaly['radius'])
        
        # Рисуем узлы (нейроны)
        for node in self.nodes:
            # Размер узла пульсирует в зависимости от активности
            size = node['size'] * (1 + 0.3 * node['activity'] * self.pulse_factor)
            
            # Градиент для узла
            gradient = QRadialGradient(node['x'], node['y'], size)
            
            # Цвет и яркость зависят от типа и активности
            node_color = node['color']
            gradient.setColorAt(0, node_color.lighter(150))
            gradient.setColorAt(0.7, node_color)
            gradient.setColorAt(1, node_color.darker(150))
            
            painter.setBrush(gradient)
            painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
            painter.drawEllipse(QPointF(node['x'], node['y']), size, size)
            
            # Рисуем название процесса
            painter.setFont(QFont("Segoe UI", 8))
            painter.setPen(QPen(QColor(255, 255, 255, 200), 1))
            painter.drawText(QRectF(node['x'] - 50, node['y'] + size + 5, 100, 20), 
                           Qt.AlignHCenter, node['name'])
    
    def mousePressEvent(self, event):
        """Обработка нажатия кнопки мыши"""
        if event.button() == Qt.LeftButton:
            self.is_panning = True
            self.last_mouse_pos = event.pos()
    
    def mouseReleaseEvent(self, event):
        """Обработка отпускания кнопки мыши"""
        if event.button() == Qt.LeftButton:
            self.is_panning = False
    
    def mouseMoveEvent(self, event):
        """Обработка движения мыши"""
        if self.is_panning and self.last_mouse_pos:
            # Перемещение карты
            delta = event.pos() - self.last_mouse_pos
            self.pan_offset_x += delta.x()
            self.pan_offset_y += delta.y()
            self.last_mouse_pos = event.pos()
            self.update()
    
    def wheelEvent(self, event):
        """Обработка прокрутки колеса мыши (масштабирование)"""
        zoom_factor = 1.1
        
        if event.angleDelta().y() > 0:
            # Увеличение масштаба
            self.zoom_level *= zoom_factor
        else:
            # Уменьшение масштаба
            self.zoom_level /= zoom_factor
        
        # Ограничиваем масштаб
        self.zoom_level = max(0.5, min(3.0, self.zoom_level))
        self.update()


# Тестирование виджета
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    
    # Создаем нейронную карту
    neural_map = NeuralEcosystemMap()
    layout.addWidget(neural_map)
    
    window.setLayout(layout)
    window.setWindowTitle("Нейронная карта экосистемы")
    window.resize(800, 600)
    window.show()
    
    sys.exit(app.exec_()) 