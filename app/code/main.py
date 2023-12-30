import logging

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, text, func
from data_model import User, ProductCard, PurchaseItem, PurchaseHistory, ItemCart

# Create an engine and create tables if they don't exist
engine_url = "mariadb+mariadbconnector://root:root@mariadb/api_db" # access from docker network
engine = create_engine(engine_url)
# Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()

logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test database connection
@app.get("/test-db-connection")
async def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Try to create a session
        db.execute(text("SELECT 1"))
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"message": f"Database connection error: {str(e)}"}



# Endpoint to create a new user
@app.post("/users/create/", status_code=201)
async def create_user(username: str, password: str, first_name: str, last_name: str, email: str, is_seller: bool, db: Session = Depends(get_db)):
    try:
        new_user = User(
            username=str(username).strip(),
            password=str(password).strip(),
            first_name=str(first_name).strip(),
            last_name=str(last_name).strip(),
            email=str(email).strip(),
            is_seller=bool(is_seller)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()

        return {"message": "User created successfully", "username": username}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to search for a user by login
@app.get("/users/")
async def get_user_by_login(login: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == login).first()

        if user:
            return user.__dict__
            # return {"user_id": user.user_id,
            #         "username": user.username,
            #         "password": user.password,
            #         "first_name": user.first_name,
            #         "last_name": user.last_name,
            #         "email": user.email,
            #         "is_seller": user.is_seller,
            #         "created_at": user.created_at,
            #         "updated_at": user.updated_at
            #         }
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        db.close()


# Endpoint to search for a user by first/last name mask
@app.get("/users/search_user_by_name_and_lastname/") 
async def search_users_by_mask(first_name: str = '', last_name: str = '', db: Session = Depends(get_db)):
    try:
        if first_name and last_name:
            users = db.query(User).filter(User.first_name.ilike(f"%{first_name}%"), User.last_name.ilike(f"%{last_name}%")).all()
        elif first_name:
            users = db.query(User).filter(User.first_name.ilike(f"%{first_name}%")).all()
        elif last_name:
            users = db.query(User).filter(User.last_name.ilike(f"%{last_name}%")).all()
        else:
            raise HTTPException(status_code=400, detail="Please provide a first name and/or last name")

        if users:
            return {"matched_users": [user for user in users]}
        else:
            raise HTTPException(status_code=404, detail="No users found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to check if seller has unique product card by product title
@app.get("/products/check_seller_card/")
async def check_seller_unique_card(user_id: str, card_title: str, db: Session = Depends(get_db)):
    try:
        cards = db.query(ProductCard).filter(ProductCard.seller_id == user_id, 
                                         ProductCard.title == card_title).all()
        # return cards
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(cards) >= 1:
        return False
    else:
        return True
    
    

## Endpoint to create a product card
@app.post("/products/create/")
async def create_product_card(title: str, description: str, category: str, price: float, login: str, db: Session = Depends(get_db)):
    try:
        # get user to check if he's a buyer
        user = await get_user_by_login(login, db)
        # logger.info(f"User type: {type(user)}")
        if not user['is_seller']:
            raise HTTPException(status_code=403, detail="Unauthorized: User is not a seller")
        # return title
        if not await check_seller_unique_card(user['user_id'], title, db):
            raise HTTPException(status_code=403, detail="Seller already has such item card. To update it's attributes use corresponding function")

        new_card = ProductCard(
            seller_id=int(user['user_id']),
            title=str(title).strip(),
            description=str(description).strip(),
            category=str(category).strip(),
            price=round(float(price), 2)
        )

        db.add(new_card)
        db.commit()
        db.refresh(new_card)
        db.close()

        return {"message": f"Product card created successfully", "card": new_card.__dict__, "user": user} 
    except Exception as e:
        logger.exception("Error occurred during product card creation")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to search for a product card by id
@app.get("/products/}")
async def get_product_card_by_id(card_id: str, db: Session = Depends(get_db)):
    try:
        card = db.query(ProductCard).filter(ProductCard.product_id == card_id).first()

        if card:
            return card.__dict__
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Function to update a product card
@app.put("/products/update/")
async def update_product_card(
    login: str,
    product_id: int,
    title: str,
    description: str = None,
    category: str = None,
    price: float = None,
    db: Session = Depends(get_db)
    ):

    try:
        # get user to check if he's a buyer
        user = await get_user_by_login(login, db)
        product_card = db.query(ProductCard).filter(ProductCard.product_id == product_id).first()

        # logger.info(f"User type: {type(user)}")
        if not user['is_seller']:
            raise HTTPException(status_code=403, detail="Unauthorized: User is not a seller")
        
        # Check permissions to update card update (only creator can change it)
        elif product_card is None:
            raise HTTPException(status_code=404, detail="Product card not found")
    
        elif product_card.seller_id != user['user_id']:
            raise HTTPException(status_code=403, detail="Unauthorized: User doesn't have permission to modify this card")
    
        product_card.title = title
        if description:
            product_card.description = description
        
        if category:
            product_card.category = category
        
        if price:
            product_card.price = price

        db.commit()
        db.refresh(product_card)
        db.close()

        return {"message": f"Product card updated successfully", "card": product_card.__dict__, "user": user} 

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

# Function to delete a product card
@app.delete("/products/remove/")
async def delete_product_card(
    product_id: int,
    login: str,
    db: Session = Depends(get_db)
):

    try:
        # get user to check if he's a buyer
        user = await get_user_by_login(login, db)
        product_card = db.query(ProductCard).filter(ProductCard.product_id == product_id).first()

        if not user['is_seller']:
            raise HTTPException(status_code=403, detail="Unauthorized: User is not a seller")
        
        # Check permissions to update card update (only creator can change it)
        elif product_card is None:
            raise HTTPException(status_code=404, detail="Product card not found")
    
        elif product_card.seller_id != user['user_id']:
            raise HTTPException(status_code=403, detail="Unauthorized: User doesn't have permission to delete this card")

       
        db.delete(product_card)
        db.commit()

        return {"message": "Product card deleted successfully", "user": user, "card": product_card.__dict__}

    except Exception as e:
        db.rollback()  # Rollback changes in case of an error
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()  # Close the database session


# Function to get all available products for the main page
@app.get("/home")
async def get_all_products(db: Session = Depends(get_db)):
    """
    All users get same infinite list of available products
    """
    try:
        # Retrieve all products from the ProductCard table
        products = db.query(ProductCard).all()

        return products

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()  # Close the database session


# Dummy recsys
@app.get("/highlights")
async def get_recommendation(db: Session = Depends(get_db)):
    """
    Function returns top 10 relevant product cards for a user
    (Now is dummy function that return randoms cards so that probability of successfull conversion would be about 50%)
    """
    try:
        products = db.query(ProductCard).order_by(func.random()).limit(10).all()
        prods = [prod.__dict__ for prod in products]

        return prods
    
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
    finally:
        db.close()



@app.post("/cart/add_to_cart/", status_code=201)
async def add_item_to_user_cart(user_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    """
    Function adds product_id and it's quantity to ItemCart table. Unique_key - user_id, product_id
    """
    try:
        new_item = ItemCart(
            user_id = user_id,
            product_id = product_id,
            quantity = quantity
        )

        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        db.close()

        return {"message": "New item added successfully to User cart", "item": new_item.__dict__}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
    finally:
        db.close()


@app.delete("/cart/delete_from_cart/", status_code=201)
async def delete_item_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    """
    Function removes product_id from user Cart on (user_id, product_id) key
    """
    try:
        # get item from user cart
        product_card = db.query(ItemCart).filter(ItemCart.product_id == product_id,
                                                 ItemCart.user_id == user_id).first()

        if not product_card:
            raise HTTPException(status_code=500, detail="No such item found in user cart")

        db.delete(product_card)
        db.commit()

        return {"message": "Item removed successfully from UerCart", "user_id": user_id, "removed_item": product_card.__dict__}

    except Exception as e:
        db.rollback()  # Rollback changes in case of an error
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()  # Close the database session


@app.delete("/cart/delete_user_cart/", status_code=201)
async def delete_user_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Function removes user cart from ItemCart table on user_id key (delete all products_id for given user)
    """
    try:
        # get item from user cart
        item_cart = db.query(ItemCart).filter(ItemCart.user_id == user_id).all()
        # return {"check item card to delete": [item.__dict__ for item in item_cart]}
        if not item_cart:
            raise HTTPException(status_code=500, detail="User cart not found")

        for item in item_cart:
            db.delete(item)
        
        db.commit()

        return {"message": "User cart successfully removed from UerCart", "user_id": user_id, "removed_cart": [item.__dict__ for item in item_cart]}

    except Exception as e:
        db.rollback()  # Rollback changes in case of an error
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@app.put("/cart/update_item_quantity/", status_code=201)
async def add_one_item_in_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    """
    Function updates amount of product_id in user cart
    """
    try:
        product_card = db.query(ItemCart).filter(ItemCart.product_id == product_id,
                                                 ItemCart.user_id == user_id).first()
        
        if not product_card:
            raise HTTPException(status_code=500, detail="No such item found in user cart")

        product_card.quantity += 1

        db.commit()
        db.refresh(product_card)
        db.close()

        return {"message": "Successfully added one item in your cart", "user_id": user_id, "product_id": product_id, "card": product_card.__dict__} 

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/cart/get_user_cart/")
async def get_user_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Function gets all items in user's cart
    Returns: List[dict]
    """
    try:
        # Retrieve all user products from the ItemCart table
        user_cart = db.query(ItemCart, ProductCard).filter(ItemCart.product_id == ProductCard.product_id).filter(ItemCart.user_id == user_id).all()
        
        if not user_cart:
            raise HTTPException(status_code=500, detail="User cart not found")
        

        # Pack cart and price in the         
        user_cart_list = []
        for item_cart, product_card in user_cart:
            # Retrieve item_cart details and product price and pack it in PurchaseItem class
            user_cart_list.append(
                {
                    "product_id": item_cart.product_id,
                    "quantity": item_cart.quantity,
                    "price": product_card.price
                }
            )
            
        return {'user_id': user_id, 'cart': user_cart_list}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@app.post("/cart/buy")
async def make_purchase(user_id: int, db: Session = Depends(get_db)):
    """
    Function does steps as follows:
        1. Generate purchase_id by inserting user_id into PurchaseHistory table and instantly getting this row back
        2. Get ItemCart of a user by user_id and adds actual product price from ProductCards catalog
        3. Remove user's cart from ItemCart 
    """

    try:
        # Step 1
        purchase_record = PurchaseHistory(buyer_id = user_id) 

        db.add(purchase_record)
        db.commit()
        db.refresh(purchase_record)
        # db.close()

        # Step 2
        # Query to join ItemCart with ProductCard based on product_id
        
        user_cart = await get_user_cart(user_id, db)
        
        # List to hold the result of user's grocery cart with product prices
        inserted_user_cart = []

        for elem in user_cart['cart']:
            purchase_item_record = PurchaseItem(
                purchase_id = purchase_record.purchase_id,
                product_id = elem['product_id'],
                quantity = elem['quantity'],
                price = elem['price']
            )
            

            # insert record into PurchaseItems table
            db.add(purchase_item_record)
            db.commit()
            db.refresh(purchase_item_record)

            # with added info append inserted row            
            inserted_user_cart.append(purchase_item_record.__dict__)
            
        # Step 3
        
        delete_res = await delete_user_cart(user_id, db)
        # return {"delete_card function output": delete_res}

        return {"message": "Purchase created uccessfully! Well done!", "user_id": user_id, "cart": inserted_user_cart}

    except Exception as e:        
        return HTTPException(status_code=500, detail=str(e))

# """
# Добавить функцииЖ
#     1. Добавить товар в корзину - done
#         - в таблицу ItemCart добавляется запись с полями user_id, product_id, quantity
#     2. Удалить товар из корзины - done
#         - по паре ключей user_id, product_id удаляется запись из таблицы ItemCart
#     3. Добавить +1 товар в корзину (update) - done
#         - добавляет +1 к атрибуту quantity в таблице ItemCart по ключу user_id, product_id
#     4. Совершить покупку:
#         - Забирает корзину пользователя по ключу user_id из таблицы ItemCart. 
#             Обновляет цену на товар из актуальноно продуктового каталога (джойн с витриной ProductCards, чтобы не продавать по старым ценам)
#         - Создает запись в таблицу PurchaseHistory. Записывает user_id. Поле purchase_id, purchase_date генерируется автоматически. Функция возвращает purchase_id
#         - Делается запись клиентской корзины в таблицу PurchaseItems. Т.е. к корзине добавляется актуальная цена из справочника, id покупки, дата покупки. 
#         - Записывает продуктовую корзину в таблицу продаж (PurchaseItems) 
#         - Из витрины с корщинами удаляется текущая продуктовая корзина.
# """