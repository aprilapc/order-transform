# Order API

這是一個使用 Flask 建立的簡單 Order API，包含一個 POST `/api/orders` 的 endpoint。此 API 接收訂單資料並進行驗證，確保所有欄位都符合要求。

## 使用 python 執行

1. 安裝所需套件：
    ```sh
    pip install Flask
    ```

2. 啟動伺服器：
    ```sh
    python app.py
    ```
3. 應用程式將在 `http://localhost:8000` 運行。

## 使用 Docker 啟動

1. 構建並啟動容器：
    ```sh
    docker-compose up -d
    ```

2. 應用程式將在 `http://localhost:8000` 運行。

3. 查看 logs：
    ```sh
    docker-compose logs -f 
    ```

## API 說明

### POST /api/orders

#### 請求範例
```json
{
    "id": "A0000001",
    "name": "Melody Holiday Inn",
    "address": {
        "city": "taipei-city",
        "district": "da-an-district",
        "street": "fuxing-south-road"
    },
    "price": "2000",
    "currency": "TWD"
}
```

#### 回應範例
1. 成功：
    ```json
    {
        "message": "Order received",
        "order": {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "2000",
            "currency": "TWD"
        }
    }
    ```

2. 失敗：
    ```json
    {
      "error": "錯誤訊息"
    }
    ```

#### 錯誤訊息清單

- `Order ID is required`：order.id 必填
- `Name is required`：order.name 必填
- `Address is required`：order.address 必填
- `City is required`：order.address.city 必填
- `District is required`：order.address.district 必填
- `Street is required`：order.address.street 必填
- `Price is required`：order.price 必填
- `Currency is required`：order.currency 必填
- `Price must be a number`：order.price 必須為數字
- `Currency format is wrong`：order.currency 需為 TWD 或 USD
- `Price is over 2000`： order.price 轉換後不可超過 2000
- `Name contains non-English characters`：order.name 不可包含非英文字符
- `Name is not capitalized`：order.name 每個單字首字母需大寫

## 單元測試
1. 運行單元測試：
    ```sh
    python -m unittest test_order_service.py
    ```

## 專案結構
```
order-transform/
├── app.py
├── order.py
├── order_service.py
├── order_validator.py
├── test_order_service.py
└── README.md
```
- [app.py](app.py): Flask 應用程式的入口，定義了 API endpoint。
- [order.py](order.py): 定義了 Order 和 Address 類別。
- [order_service.py](order_service.py): 定義了 OrderService 類別，負責處理訂單格式檢查與轉換邏輯。
- [order_validator.py](order_validator.py): 定義了 OrderValidator 類別，負責驗證訂單資料欄位必填以及是否為指定型態。
- [test_order_service.py](test_order_service.py): 單元測試文件，測試 OrderService 的功能，包含所有正確及錯誤案例。
- [README.md](README.md): 專案說明文件。

## SOLID 原則
### 單一職責原則 (Single Responsibility Principle, SRP): 對象應該僅具有一種單一功能
- [app](app.py) 只負責定義 API 路由和處理 HTTP 請求。
- Order 類別負責表示訂單資料。
- Address 類別負責表示地址資料。
- [OrderValidator](order_validator.py) 類別負責驗證訂單資料欄位必填以及指定型態。
- [OrderService](order_service.py) 類別負責處理訂單格式檢查與轉換。

### 開放封閉原則 (Open/Closed Principle, OCP): 軟體應該是對於擴充開放的，但是對於修改封閉的
- [OrderValidator](order_validator.py) 和 [OrderService](order_service.py) 可以通過繼承和覆寫方法來擴展，而不需要修改現有的驗證邏輯。

### 里氏替換原則 (Liskov Substitution Principle, LSP): 程式中的對象應該是可以在不改變程式正確性的前提下被它的子類所替換的
- [OrderValidator](order_validator.py) 類別中的靜態方法 `validate` 可以被子類別覆寫，以提供不同的驗證邏輯，而不影響 [OrderValidator](order_validator.py) 的使用。

### 介面隔離原則 (Interface Segregation Principle, ISP): 多個特定客戶端介面要好於一個寬泛用途的介面
- [OrderValidator](order_validator.py) 類別只提供單一的 `validate` 方法，確保介面簡單且專注於單一職責。

### 依賴反轉原則 (Dependency Inversion Principle, DIP): 依賴於抽象而不是一個實例
- [OrderValidator](order_validator.py) 類別依賴於 [OrderValidator](order_validator.py) 介面來驗證訂單資料，而不是依賴具體的實現。

## 設計模式
### 策略模式 (Strategy Pattern) 
- 使用了策略模式來處理不同的驗證邏輯，通過將驗證邏輯封裝在 [OrderValidator](order_validator.py) 中，可以根據需要替換不同的驗證策略。

### 依賴注入 (Dependency Injection) 
- 使用了依賴注入模式來將 [OrderValidator](order_validator.py) 注入到 [OrderService](order_service.py) 中，這樣可以輕鬆替換或擴展驗證邏輯。
