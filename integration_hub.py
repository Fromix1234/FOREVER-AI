import sys
import os
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QProgressBar, QTabWidget, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QColor, QPainter, QLinearGradient

from neural_ecosystem import NeuralEcosystemMap
from quantum_signatures import QuantumSignatureVisualizer
from temporal_prediction import TemporalVisualizationWidget

class IntegrationMetrics(QObject):
    """Класс для сбора и анализа метрик от всех компонентов защиты"""
    
    metrics_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.metrics = {
            'neural': {
                'anomaly_score': 0.0,
                'system_health': 100.0,
                'active_threats': 0
            },
            'quantum': {
                'signature_matches': 0,
                'suspicious_files': 0,
                'confidence_level': 0.0
            },
            'temporal': {
                'threat_probability': 0.0,
                'prediction_accuracy': 0.0,
                'risk_level': 'Low'
            }
        }
        
        # История метрик для анализа трендов
        self.metrics_history = []
        
        # Максимальное количество исторических записей
        self.max_history = 1000
    
    def update_metrics(self, component: str, new_metrics: dict):
        """Обновляет метрики для указанного компонента"""
        if component in self.metrics:
            self.metrics[component].update(new_metrics)
            
            # Сохраняем текущее состояние в истории
            self.metrics_history.append({
                'timestamp': datetime.now(),
                'metrics': self.metrics.copy()
            })
            
            # Ограничиваем размер истории
            if len(self.metrics_history) > self.max_history:
                self.metrics_history.pop(0)
            
            # Уведомляем об обновлении
            self.metrics_updated.emit(self.metrics)
    
    def get_threat_level(self) -> float:
        """Рассчитывает общий уровень угрозы на основе всех метрик"""
        neural_threat = (100 - self.metrics['neural']['system_health']) / 100
        quantum_threat = self.metrics['quantum']['suspicious_files'] / 100
        temporal_threat = {
            'Low': 0.2,
            'Medium': 0.5,
            'High': 0.8,
            'Critical': 1.0
        }.get(self.metrics['temporal']['risk_level'], 0.0)
        
        # Взвешенная сумма всех факторов
        return (neural_threat * 0.4 + 
                quantum_threat * 0.3 + 
                temporal_threat * 0.3)
    
    def get_system_status(self) -> str:
        """Определяет текущий статус системы на основе метрик"""
        threat_level = self.get_threat_level()
        
        if threat_level < 0.2:
            return "Система безопасна"
        elif threat_level < 0.4:
            return "Требуется внимание"
        elif threat_level < 0.6:
            return "Повышенная опасность"
        elif threat_level < 0.8:
            return "Высокий риск"
        else:
            return "Критическая ситуация"

class IntegrationHub(QObject):
    """Центральный компонент для интеграции всех продвинутых систем защиты"""
    
    # Сигналы для обновления GUI
    threat_detected = pyqtSignal(str, float, str)  # тип угрозы, уверенность, источник
    system_status = pyqtSignal(dict)  # общий статус всех систем
    protection_score = pyqtSignal(float)  # общий показатель защищенности
    
    def __init__(self):
        """Инициализация хаба"""
        super().__init__()
        
        # Данные от различных компонентов
        self.neural_data = {}
        self.quantum_signatures = {}
        self.temporal_predictions = {}
        self.system_status_data = {}
        
        # Статус компонентов
        self.components_status = {
            'neural_ecosystem': False,
            'quantum_signatures': False,
            'temporal_prediction': False
        }
        
        # Веса для расчета общего показателя защищенности
        self.protection_weights = {
            'neural_ecosystem': 0.4,
            'quantum_signatures': 0.3,
            'temporal_prediction': 0.3
        }
        
        # Счетчики аномалий для обнаружения устойчивых угроз
        self.anomaly_counters = {
            'high_cpu': 0,
            'high_memory': 0,
            'disk_activity': 0,
            'network_activity': 0
        }
        
        # История угроз
        self.threat_history = []
        
        # Настройка логирования
        self._setup_logging()
    
    def _setup_logging(self):
        """Настройка логирования"""
        self.logger = logging.getLogger('IntegrationHub')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.FileHandler('integration_hub.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def update_neural_data(self, data):
        """Обновление данных от нейронной экосистемы"""
        try:
            if not isinstance(data, dict):
                raise ValueError("Neural data must be a dictionary")
                
            self.neural_data = data
            self.components_status['neural_ecosystem'] = True
            self._analyze_neural_threats()
            self._update_protection_score()
            self.logger.info("Neural Ecosystem data updated successfully")
        except Exception as e:
            self.logger.error(f"Error updating neural data: {str(e)}")
            self.components_status['neural_ecosystem'] = False
            
    def update_system_status(self, status_info):
        """Обновление общего статуса системы"""
        try:
            if not isinstance(status_info, dict):
                raise ValueError("Status info must be a dictionary")
                
            self.system_status_data = status_info
            
            # Получаем данные о CPU и памяти
            cpu_percent = status_info.get('cpu_percent', 0)
            mem_percent = status_info.get('memory_percent', 0)
            
            # Обновляем счетчики аномалий
            if cpu_percent > 80:  # Высокая загрузка CPU
                self.anomaly_counters['high_cpu'] += 1
            else:
                self.anomaly_counters['high_cpu'] = max(0, self.anomaly_counters['high_cpu'] - 1)
                
            if mem_percent > 85:  # Высокое использование памяти
                self.anomaly_counters['high_memory'] += 1
            else:
                self.anomaly_counters['high_memory'] = max(0, self.anomaly_counters['high_memory'] - 1)
            
            # Обнаруживаем постоянные аномалии
            for counter_name, counter_value in self.anomaly_counters.items():
                if counter_value > 5:  # Аномалия сохраняется более 5 обновлений
                    threat_confidence = min(counter_value / 10, 0.9)  # Максимум 90% уверенности
                    self.threat_detected.emit(
                        f"system_{counter_name}",
                        threat_confidence,
                        "system_monitor"
                    )
            
            self.logger.info("System status updated")
        except Exception as e:
            self.logger.error(f"Error updating system status: {str(e)}")
    
    def _analyze_neural_threats(self):
        """Анализ угроз на основе данных нейронной экосистемы"""
        try:
            if not self.neural_data:
                return
                
            # Анализируем процессы на аномалии
            processes = self.neural_data.get("processes", [])
            
            for process in processes:
                # Проверяем высокие показатели использования ресурсов
                cpu_usage = process.get("cpu", 0)
                memory_usage = process.get("memory", 0)
                process_name = process.get("name", "unknown")
                
                # Подозрительные имена процессов (пример)
                suspicious_names = ['cryptominer', 'hidden', 'stealer', 'trojan']
                
                # Проверяем имя процесса на подозрительность
                name_score = 0
                for sus_name in suspicious_names:
                    if sus_name in process_name.lower():
                        name_score = 0.8
                        break
                
                # Проверяем использование ресурсов
                resource_score = 0
                if cpu_usage > 80 and memory_usage > 500:  # Больше 80% CPU и 500MB RAM
                    resource_score = 0.7
                elif cpu_usage > 90 or memory_usage > 1000:  # Больше 90% CPU или 1GB RAM
                    resource_score = 0.6
                
                # Если есть подозрения, генерируем сообщение о угрозе
                total_score = max(name_score, resource_score)
                if total_score > 0.5:
                    self.threat_detected.emit(
                        "suspicious_process", 
                        total_score,
                        "neural_ecosystem"
                    )
                    
                    # Записываем угрозу в историю
                    self._record_threat({
                        "type": "suspicious_process",
                        "confidence": total_score,
                        "source": "neural_ecosystem",
                        "details": {
                            "process_name": process_name,
                            "pid": process.get("id"),
                            "cpu": cpu_usage,
                            "memory": memory_usage
                        },
                        "timestamp": datetime.now().isoformat()
                    })
        except Exception as e:
            self.logger.error(f"Error analyzing neural threats: {str(e)}")
    
    def update_quantum_signature(self, file_path, signature_data):
        """Обновление квантовой сигнатуры файла"""
        try:
            if not isinstance(signature_data, dict):
                raise ValueError("Signature data must be a dictionary")
            
            self.quantum_signatures[file_path] = signature_data
            self.components_status['quantum_signatures'] = True
            self._analyze_quantum_threats()
            self._update_protection_score()
            self.logger.info(f"Quantum signature updated for {file_path}")
        except Exception as e:
            self.logger.error(f"Error updating quantum signature: {str(e)}")
            self.components_status['quantum_signatures'] = False
    
    def update_temporal_prediction(self, prediction_data):
        """Обновление данных временного прогнозирования"""
        try:
            if not isinstance(prediction_data, dict):
                raise ValueError("Prediction data must be a dictionary")
                
            self.temporal_predictions = prediction_data
            self.components_status['temporal_prediction'] = True
            self._analyze_temporal_threats()
            self._update_protection_score()
            self.logger.info("Temporal prediction data updated successfully")
        except Exception as e:
            self.logger.error(f"Error updating temporal prediction: {str(e)}")
            self.components_status['temporal_prediction'] = False
    
    def _analyze_quantum_threats(self):
        """Анализ угроз на основе квантовых сигнатур"""
        for file_path, signature in self.quantum_signatures.items():
            if signature.get('uniqueness_score', 0) > 0.9:
                self.threat_detected.emit(
                    'Подозрительная квантовая сигнатура',
                    signature['uniqueness_score'],
                    'Quantum Signatures'
                )
                self._record_threat({
                    'type': 'quantum_anomaly',
                    'source': 'quantum_signatures',
                    'timestamp': datetime.now().isoformat(),
                    'details': {
                        'file_path': file_path,
                        'uniqueness_score': signature['uniqueness_score']
                    }
                })
    
    def _analyze_temporal_threats(self):
        """Анализ угроз на основе временных прогнозов"""
        if not self.temporal_predictions:
            return
        
        future_threats = self.temporal_predictions.get('future_threats', [])
        for threat in future_threats:
            if threat.get('probability', 0) > 0.7:
                self.threat_detected.emit(
                    'Прогноз потенциальной угрозы',
                    threat['probability'],
                    'Temporal Prediction'
                )
                self._record_threat({
                    'type': 'predicted_threat',
                    'source': 'temporal_prediction',
                    'timestamp': datetime.now().isoformat(),
                    'details': threat
                })
    
    def _update_protection_score(self):
        """Обновление общего показателя защищенности"""
        total_score = 0
        active_components = 0
        total_weight = 0
        
        for component, status in self.components_status.items():
            if status:
                weight = self.protection_weights[component]
                total_weight += weight
                if component == 'neural_ecosystem':
                    score = self._calculate_neural_score()
                elif component == 'quantum_signatures':
                    score = self._calculate_quantum_score()
                else:  # temporal_prediction
                    score = self._calculate_temporal_score()
                
                total_score += score * weight
                active_components += 1
        
        if active_components > 0 and total_weight > 0:
            final_score = total_score / total_weight
            self.protection_score.emit(final_score)
            
            # Обновляем статус систем
            current_status = {
                'protection_score': final_score,
                'active_components': active_components,
                'components': self.components_status.copy(),
                'threat_count': len(self.threat_history),
                'last_update': datetime.now().isoformat()
            }
            self.system_status.emit(current_status)
            return final_score
        return 0.0
    
    def _calculate_neural_score(self):
        """Расчет оценки защиты на основе данных нейронной экосистемы"""
        if not self.neural_data:
            return 0.0
        
        # Анализируем здоровье системы
        system_health = self.neural_data.get('system_health', 0.0)
        anomaly_count = sum(1 for p in self.neural_data.get('processes', {}).values() 
                          if p.get('anomaly_score', 0) > 0.8)
        
        # Нормализуем оценку
        base_score = system_health * 0.7
        anomaly_penalty = min(0.3, anomaly_count * 0.1)
        return max(0.0, base_score - anomaly_penalty)
    
    def _calculate_quantum_score(self):
        """Расчет показателя защищенности на основе квантовых сигнатур"""
        if not self.quantum_signatures:
            return 0.5  # Средний показатель по умолчанию
            
        # Анализируем данные сигнатур
        uniqueness_scores = []
        confidence_scores = []
        
        # Собираем показатели из всех сигнатур
        for file_path, signature_data in self.quantum_signatures.items():
            if isinstance(signature_data, dict):
                uniqueness = signature_data.get('uniqueness', 0.5)
                confidence = signature_data.get('confidence', 0.5)
                
                uniqueness_scores.append(uniqueness)
                confidence_scores.append(confidence)
        
        # Если нет данных, возвращаем средний показатель
        if not uniqueness_scores or not confidence_scores:
            return 0.5
            
        # Вычисляем среднее значение
        avg_uniqueness = sum(uniqueness_scores) / len(uniqueness_scores)
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        # Общий показатель - взвешенное среднее
        return (avg_uniqueness * 0.7) + (avg_confidence * 0.3)
    
    def _calculate_temporal_score(self):
        """Расчет показателя защищенности на основе временных прогнозов"""
        if not self.temporal_predictions:
            return 0.5  # Средний показатель по умолчанию
        
        # Получаем данные прогнозов
        history = self.temporal_predictions.get('history', [])
        
        if not history:
            return 0.5
            
        # Анализируем историю угроз за последние дни
        threat_counts = []
        for day_data in history[:7]:  # Берем только последние 7 дней
            if isinstance(day_data, dict):
                count = day_data.get('count', 0)
                threat_counts.append(count)
        
        if not threat_counts:
            return 0.5
            
        # Вычисляем среднее количество угроз в день
        avg_threats = sum(threat_counts) / len(threat_counts)
        
        # Нормализуем: 0 угроз -> 1.0, 10+ угроз -> 0.0
        normalized_score = max(0.0, 1.0 - (avg_threats / 10.0))
        
        return normalized_score
    
    def _record_threat(self, threat_data):
        """Запись информации об угрозе в историю"""
        self.threat_history.append(threat_data)
        self.logger.warning(f"New threat recorded: {json.dumps(threat_data)}")
        
        # Ограничиваем размер истории
        if len(self.threat_history) > 1000:
            self.threat_history = self.threat_history[-1000:]
    
    def get_threat_statistics(self):
        """Получение статистики угроз"""
        if not self.threat_history:
            return {}
        
        # Группируем угрозы по типам
        threat_types = {}
        for threat in self.threat_history:
            threat_type = threat['type']
            if threat_type not in threat_types:
                threat_types[threat_type] = 0
            threat_types[threat_type] += 1
        
        # Рассчитываем временные тренды
        current_time = datetime.now()
        recent_threats = [t for t in self.threat_history 
                        if (current_time - datetime.fromisoformat(t['timestamp'])).days < 7]
        
        return {
            'total_threats': len(self.threat_history),
            'threat_types': threat_types,
            'recent_threats': len(recent_threats),
            'threat_trend': len(recent_threats) / 7.0  # среднее количество угроз в день
        }
    
    def get_component_status(self):
        """Получение статуса всех компонентов"""
        return {
            'components': self.components_status,
            'protection_score': self._update_protection_score(),
            'last_update': datetime.now().isoformat()
        }

class IntegrationWidget(QWidget):
    """Виджет для отображения статуса интеграции"""
    
    def __init__(self, integration_hub, parent=None):
        super().__init__(parent)
        self.hub = integration_hub
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel("Интеграционный центр")
        title.setStyleSheet("""
            font-size: 18px;
            color: #64ffda;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(title)
        
        # Статус компонентов
        self.status_frame = QFrame()
        self.status_frame.setStyleSheet("""
            QFrame {
                background: rgba(20, 27, 51, 0.7);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        status_layout = QVBoxLayout(self.status_frame)
        
        # Индикаторы статуса компонентов
        self.component_indicators = {}
        for component in ['neural_ecosystem', 'quantum_signatures', 'temporal_prediction']:
            indicator = QLabel()
            indicator.setStyleSheet("color: #ff5555;")  # Изначально красный
            self.component_indicators[component] = indicator
            status_layout.addWidget(indicator)
        
        layout.addWidget(self.status_frame)
        
        # Общий показатель защиты
        protection_layout = QHBoxLayout()
        self.protection_bar = QProgressBar()
        self.protection_bar.setRange(0, 100)
        self.protection_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #2a3552;
                border-radius: 5px;
                text-align: center;
                background: #0a0d1f;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #64ffda, stop:1 #3d4b7c);
                border-radius: 3px;
            }
        """)
        protection_layout.addWidget(QLabel("Уровень защиты:"))
        protection_layout.addWidget(self.protection_bar)
        layout.addLayout(protection_layout)
        
        # Статистика угроз
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("""
            color: #8892b0;
            padding: 10px;
            background: rgba(20, 27, 51, 0.5);
            border-radius: 5px;
        """)
        layout.addWidget(self.stats_label)
    
    def connect_signals(self):
        """Подключение сигналов"""
        self.hub.system_status.connect(self.update_status)
        self.hub.protection_score.connect(self.update_protection_score)
        self.hub.threat_detected.connect(self.show_threat)
    
    def update_status(self, status):
        """Обновление отображения статуса"""
        if not isinstance(status, dict):
            return
            
        for component, indicator in self.component_indicators.items():
            is_active = status.get('components', {}).get(component, False)
            if is_active:
                indicator.setText(f"✓ {component.replace('_', ' ').title()}: Активен")
                indicator.setStyleSheet("color: #64ffda;")
            else:
                indicator.setText(f"✗ {component.replace('_', ' ').title()}: Неактивен")
                indicator.setStyleSheet("color: #ff5555;")
        
        # Обновляем статистику
        try:
            stats = self.hub.get_threat_statistics()
            stats_text = f"""
                Всего угроз: {stats.get('total_threats', 0)}
                Последние 7 дней: {stats.get('recent_threats', 0)}
                Тренд: {stats.get('threat_trend', 0):.1f} угроз/день
            """
            self.stats_label.setText(stats_text)
        except Exception as e:
            self.stats_label.setText("Ошибка получения статистики")
            logging.error(f"Error updating statistics: {str(e)}")
    
    def update_protection_score(self, score):
        """Обновление показателя защиты"""
        self.protection_bar.setValue(int(score * 100))
        
        # Меняем цвет в зависимости от уровня защиты
        if score >= 0.8:
            color = "#64ffda"  # Зеленый
        elif score >= 0.6:
            color = "#ffd700"  # Желтый
        else:
            color = "#ff5555"  # Красный
        
        self.protection_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #2a3552;
                border-radius: 5px;
                text-align: center;
                background: #0a0d1f;
            }}
            QProgressBar::chunk {{
                background: {color};
                border-radius: 3px;
            }}
        """)
    
    def show_threat(self, threat_type, confidence, source):
        """Отображение информации об обнаруженной угрозе"""
        # В будущем здесь можно добавить всплывающие уведомления или
        # другие способы информирования о новых угрозах

# Тестирование
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль приложения
    app.setStyle("Fusion")
    
    # Создаем главное окно
    main_window = QMainWindow()
    
    # Создаем Integration Hub и его виджет
    hub = IntegrationHub()
    widget = IntegrationWidget(hub)
    
    # Устанавливаем виджет в главное окно
    main_window.setCentralWidget(widget)
    main_window.setWindowTitle("ForeverAI Integration Hub")
    main_window.resize(800, 600)
    main_window.show()
    
    # Запускаем мониторинг
    hub.update_neural_data({})  # Инициализируем пустыми данными
    hub.update_quantum_signature("test", {})
    hub.update_temporal_prediction({})
    
    sys.exit(app.exec_()) 