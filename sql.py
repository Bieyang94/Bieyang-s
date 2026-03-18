from sqlmodel import SQLModel, Field, create_engine
import sqlmodel
from sqlmodel import Session, select
from typing import List, Optional
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.vectorstores.base import VectorStoreRetriever

class AI_train(SQLModel, table=True):
    """AI训练数据基础模型"""
    __tablename__ = "ai_train"
    num: int = Field(primary_key=True, default_factory=None)
    image: str    

sqlite_url = "sqlite:///AImj.db"

class AI_trainCRUD:
    def __init__(self, db_url: str = sqlite_url):    
        """初始化数据库引擎"""
        self.engine = create_engine(sqlite_url, echo=True)
        self.create_db_and_tables()
    
    def create_db_and_tables(self):
        """创建数据库和表"""
        SQLModel.metadata.create_all(self.engine)
        print("数据库表创建成功！")
    
    # 创建操作
    def create_image(self, image: AI_train) -> AI_train:
        """创建新的AI训练数据"""
        with Session(self.engine) as session:
            db_image = AI_train.model_validate(image)
            session.add(db_image)
            session.commit()
            session.refresh(db_image)
            print(f"AI训练数据创建成功: {db_image.num}")
            return db_image
    
    def create_images_bulk(self, images: List[AI_train]) -> List[AI_train]:
        """批量创建AI训练数据"""    
        with Session(self.engine) as session:
            db_images = [AI_train.model_validate(image) for image in images]
            session.add_all(db_images)
            session.commit()
            for image in db_images:
                session.refresh(image)
            print(f"批量创建 {len(db_images)} 个AI训练数据成功")
            return db_images
    
    # 读取操作
    def get_all_images(self) -> List[AI_train]:
        """获取所有AI训练数据"""
        with Session(self.engine) as session:
            statement = select(AI_train)
            images = session.exec(statement).all()
            print(f"共获取 {len(images)} 个AI训练数据")
            return images
    
    def get_image(self, image_id: int) -> Optional[AI_train]:
        """根据ID获取AI训练数据"""
        with Session(self.engine) as session:
            statement = select(AI_train).where(AI_train.num == image_id)
            image = session.exec(statement).first()
            if image:
                print(f"找到AI训练数据: {image.num}")
            else:
                print(f"未找到ID为 {image_id} 的AI训练数据")
            return image
    
    # 更新操作
    def update_image(self, image_id: int, updated_image: AI_train) -> Optional[AI_train]:
        """更新AI训练数据"""
        with Session(self.engine) as session:
            statement = select(AI_train).where(AI_train.num == image_id)
            image = session.exec(statement).first()
            if image:
                for key, value in updated_image.model_dump(exclude_unset=True).items():
                    setattr(image, key, value)
                session.commit()
                session.refresh(image)
                print(f"AI训练数据更新成功: {image.num}")
            else:
                print(f"未找到ID为 {image_id} 的AI训练数据")
            return image
    
    # 删除操作
    def delete_image(self, image_id: int) -> bool:
        """根据ID删除AI训练数据"""
        with Session(self.engine) as session:
            statement = select(AI_train).where(AI_train.num == image_id)
            image = session.exec(statement).first()
            if image:
                session.delete(image)
                session.commit()
                print(f"AI训练数据删除成功: {image_id}")
                return True
            else:
                print(f"未找到ID为 {image_id} 的AI训练数据")
                return False
    

if __name__ == "__main__":
    ai_train_crud = AI_trainCRUD()
    # 测试创建操作
    new_image = AI_train(num=1, image="test_image_data")
    created_image = ai_train_crud.create_image(new_image)
    print(created_image)
    
