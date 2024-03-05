from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRectF, Qt, QPointF ,QLineF ,QSize
from PyQt5.QtGui import QPainterPath, QPainter, QPen, QBrush,QFont, QColor ,QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from typing import List, Tuple

class LabelItem():
    label = None
    # Movement = None



class MyPointItem(QGraphicsEllipseItem, LabelItem):
    EditMode = False
    def __init__(self, x, y, radius=5, parent=None):
        super().__init__(parent)
        self.setPos(x, y)
        self.setRect(-radius, -radius, radius*2, radius*2)
        self.setBrush(QBrush(QColor(255, 0, 0)))
        self.pen = QPen(Qt.NoPen)
        self.setPen(self.pen)
        self.setFlag(self.ItemIsSelectable)
        self.setFlag(self.ItemIsMovable)
        
    def mousePressEvent(self, event):
        if self.EditMode:
            pos = event.scenePos()
            self.startPos = pos
            self.item_pos = self.pos()

    def mouseMoveEvent(self, event):
        if self.EditMode and not self.OutofBoundary(event):
            if event.buttons() == Qt.LeftButton:
                self.setPos(self.pos() + event.pos() - event.lastPos())     

    def OutofBoundary(self,event):
        bounds_rect = self.scene().sceneRect()
        new_pos = self.pos() + event.pos() - event.lastPos()
        if not bounds_rect.contains(new_pos)  :
            return True
        return False
    
    def setLineColor(self, color):
        brush = self.brush()
        brush.setColor(QColor(color))
        self.setBrush(brush)
        self.pen.setColor(QColor(color))
        self.update()

    def getAllpoints(self):
        points=[]
        points.append(self.pos())
        return points
    
class LinePoint(QGraphicsEllipseItem, LabelItem):
    EditMode = False
    def __init__(self, x, y, radius=5, parent=None):
        super().__init__(parent)
        self.setPos(x, y)
        self.setRect(-radius, -radius, radius*2, radius*2)
        self.setBrush(QBrush(QColor(255, 0, 0)))
        self.setFlags(QGraphicsEllipseItem.ItemIsMovable | QGraphicsEllipseItem.ItemSendsScenePositionChanges)

    def itemChange(self, change, value):
        if not self.parentItem().isSelected():
            if isinstance(self.parentItem(), MyLineStrip) and  change == QGraphicsEllipseItem.ItemScenePositionHasChanged:
                new_pos = value
                bounds_rect = self.parentItem().scene().sceneRect()
                if not bounds_rect.contains(new_pos)  :
                    # 如果超出邊界，將新位置更改為邊界內的最近位置
                    new_pos.setX(min(bounds_rect.right(), max(bounds_rect.left(), new_pos.x())))
                    new_pos.setY(min(bounds_rect.bottom(), max(bounds_rect.top(), new_pos.y())))
                    self.setPos(new_pos) 
                self.parentItem().updatePath() 
            elif isinstance(self.parentItem(), MyLineItem) and change == QGraphicsEllipseItem.ItemScenePositionHasChanged:
                new_pos = value
                bounds_rect = self.parentItem().scene().sceneRect()
                if not bounds_rect.contains(new_pos)  :
                    # 如果超出邊界，將新位置更改為邊界內的最近位置
                    new_pos.setX(min(bounds_rect.right(), max(bounds_rect.left(), new_pos.x())))
                    new_pos.setY(min(bounds_rect.bottom(), max(bounds_rect.top(), new_pos.y())))
                    self.setPos(new_pos) 
                self.parentItem().updatePath() 
            elif isinstance(self.parentItem(), MyRectItem) and change == QGraphicsEllipseItem.ItemScenePositionHasChanged:
                new_pos = value
                bounds_rect = self.parentItem().scene().sceneRect()
                if not bounds_rect.contains(new_pos)  :
                    # 如果超出邊界，將新位置更改為邊界內的最近位置
                    new_pos.setX(min(bounds_rect.right(), max(bounds_rect.left(), new_pos.x())))
                    new_pos.setY(min(bounds_rect.bottom(), max(bounds_rect.top(), new_pos.y())))
                    self.setPos(new_pos) 
                self.parentItem().updatePath()    
        return super().itemChange(change, value)
               
class MyRectItem(QGraphicsPathItem, LabelItem):
    EditMode = False
    def __init__(self, x1, y1, x2, y2,parent=None):
        super().__init__(parent)
        self.pen = QPen(QColor(0, 255, 0))
        self.pen.setWidth(3)
        self.brush = QBrush(QColor(0, 0, 0, 0))
        self.point1 = LinePoint(x1, y1, parent=self)
        self.point2 = LinePoint(x2, y2, parent=self)
    

    def updatePath(self):
        self.path = QPainterPath()
        pos1 = self.point1.scenePos()
        pos2 = self.point2.scenePos()
        pos3 = QPointF(pos2.x(),pos1.y())
        pos4 = QPointF(pos1.x(),pos2.y())
        self.path.moveTo(pos1)
        self.path.lineTo(pos3)
        self.path.lineTo(pos2)
        self.path.lineTo(pos4)
        self.path.closeSubpath()
        self.setPath(self.path)
        self.setPen(self.pen)
        self.setBrush(self.brush)

    def setStartPoint(self, x, y):
        self.point1.setPos(x, y)

    def setEndPoint(self, x, y):
        self.point2.setPos(x, y)

    def setLastPoint(self,x,y):
        self.childItems()[-1].setPos(x,y)

    def mousePressEvent(self, event):
        
        if self.EditMode:
            pos = event.scenePos()
            self.startPos = pos
            self.allItem_pos = []
            for point_item in self.childItems():
                self.allItem_pos.append(point_item.pos())
        
    def mouseMoveEvent(self, event):
        if self.EditMode and not self.OutofBoundary(event):
            for point_item in self.childItems():
                point_item.setPos(point_item.pos() + event.pos() - event.lastPos())
            self.updatePath()

    def setLineColor(self, color):
        self.pen.setColor(QColor(color))
        self.updatePath()     

    def OutofBoundary(self,event):
        for point_item in self.childItems():
            bounds_rect = self.scene().sceneRect()
            new_pos = point_item.pos() + event.pos() - event.lastPos()
            if not bounds_rect.contains(new_pos)  :
                return True
        return False
    
    def getAllpoints(self):
        points=[]
        for point_item in self.childItems():  
            points.append(point_item.pos())
        return points
    
class MyLineItem(QGraphicsLineItem, LabelItem):
    EditMode = False
    def __init__(self, x1, y1, x2, y2,parent=None):
        super().__init__(x1, y1, x2, y2, parent)
        self.pen = QPen(QColor(Qt.black))
        self.pen.setWidth(3)
        self.setPen(self.pen)
        self.point1 = LinePoint(x1, y1, parent=self)
        self.point2 = LinePoint(x2, y2, parent=self)

    def updatePath(self):
        start = self.point1.scenePos()
        end = self.point2.scenePos()
        self.setLine(start.x(), start.y(), end.x(), end.y())

    def setStartPoint(self, x, y):
        self.point1.setPos(x, y)

    def setEndPoint(self, x, y):
        self.point2.setPos(x, y)

    def mousePressEvent(self, event):
        if self.EditMode:
            pos = event.scenePos()
            self.startPos = pos
            self.allItem_pos = []
            for point_item in self.childItems():
                self.allItem_pos.append(point_item.pos())

    def mouseMoveEvent(self, event):
        if self.EditMode and not self.OutofBoundary(event):
            for point_item in self.childItems():
                point_item.setPos(point_item.pos() + event.pos() - event.lastPos())
            self.updatePath()

    def setLineColor(self, color):
        pen = self.pen
        pen.setColor(QColor(color))
        self.setPen(pen)
        self.update()
        
    def OutofBoundary(self,event):
        for point_item in self.childItems():
            bounds_rect = self.scene().sceneRect()
            new_pos = point_item.pos() + event.pos() - event.lastPos()
            if not bounds_rect.contains(new_pos)  :
                return True
        return False
    
    def getAllpoints(self):
        points=[]
        for point_item in self.childItems():  
            points.append(point_item.pos())
        return points
    
class MyLineStrip(QGraphicsPathItem, LabelItem):
    EditMode = False
    def __init__(self, points: List[Tuple[float, float]], shape="linestrip", parent=None):
        super().__init__(parent)
        self.points = points
        self.shape = shape
        self.path = QPainterPath()
        self.pen = QPen(QColor(0, 0, 255)) if self.shape=="linestrip" else QPen(QColor(255, 165, 0))
        self.pen.setWidth(3)
        self.brush = QBrush(QColor(0, 0, 0, 0))
        self.initPoints()

    def initPoints(self):
        for point in self.points:
            x, y = point
            point_item = LinePoint(x, y, parent=self)
            point_item.setFlags(
                QGraphicsPathItem.ItemIsMovable | QGraphicsPathItem.ItemSendsScenePositionChanges)
            point_item.setBrush(QBrush(QColor(Qt.red)))
        self.updatePath()

    def addPoint(self, point: Tuple[float, float]):
        # 創建新的點物件，並設定其座標和相關屬性
        point_item = LinePoint(point[0], point[1], parent=self)
        point_item.setFlags(QGraphicsPathItem.ItemIsMovable | QGraphicsPathItem.ItemSendsScenePositionChanges)
        point_item.setBrush(QBrush(QColor(Qt.red)))
        point_item.setParentItem(self)
        # 在路徑中加入新的線段
        self.path.lineTo(point_item.scenePos())
        # 重新設定筆刷和路徑
        self.setPath(self.path)
        self.setPen(self.pen)
        self.setBrush(self.brush)

    def setLastPoint(self,x,y):
        self.childItems()[-1].setPos(x,y)

    def mousePressEvent(self, event):
        if self.EditMode:
            pos = event.scenePos()
            self.startPos = pos
            self.allItem_pos = []
            for point_item in self.childItems():
                self.allItem_pos.append(point_item.pos())
        
    def mouseMoveEvent(self, event):
        if self.EditMode and not self.OutofBoundary(event):
            for point_item in self.childItems():
                point_item.setPos(point_item.pos() + event.pos() - event.lastPos())
            self.updatePath()

    def setShape(self,shape : str):
        self.shape=shape

    def updatePath(self):
        self.path = QPainterPath()
        for i, point_item in enumerate(self.childItems()):
            pos = point_item.scenePos()
            if i == 0:
                self.path.moveTo(pos)
            else:
                self.path.lineTo(pos)
        if self.shape == "poly": 
            self.path.closeSubpath()
        self.setPath(self.path)
        self.setPen(self.pen)
        self.setBrush(self.brush)

    def setLineColor(self, color):
        pen = self.pen
        pen.setColor(QColor(color))
        self.setPen(pen)
        self.update()

    def OutofBoundary(self,event):
        for point_item in self.childItems():
            bounds_rect = self.scene().sceneRect()
            new_pos = point_item.pos() + event.pos() - event.lastPos()
            if not bounds_rect.contains(new_pos)  :
                return True
        return False   

    def getAllpoints(self):
        points=[]
        for point_item in self.childItems():  
            points.append(point_item.pos())
        return points
    