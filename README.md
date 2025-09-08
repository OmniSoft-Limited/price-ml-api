# Software Price Prediction AI API

![FastAPI](https://img.shields.io/badge/FastAPI-Ready-brightgreen) ![AI](https://img.shields.io/badge/AI-Prediction-blue)

## Overview

The **Software Price Prediction AI API** predicts the estimated price of software products based on input parameters. The AI model behind it is trained using the dataset and scripts available [here](https://github.com/OmniSoft-Limited/price-prediction-model/tree/main).

This API allows businesses, developers, and startups to get instant software price predictions for market analysis, budgeting, and pricing strategies.

---

## Subscription & Access

To access the API, contact **OmniSoft**:

```
Email: dev@omnisoft.ltd
```

API access is subscription-based:

| Plan     | Description                                              |
| -------- | -------------------------------------------------------- |
| **Free** | 3-day API key. Limited usage for testing and evaluation. |
| **Paid** | Unlimited API usage with full access.                    |

> After contacting OmniSoft, you’ll receive your API key. Include it in the Authorization header for requests.

---

## Features

* Predict software prices with a simple API call.
* Token-based authentication for secure access.
* Rate-limited endpoints to prevent abuse.
* Full OpenAPI documentation available.

---

## API Endpoints

### 1. **Predict Software Price**

**POST** `/ai/predict`

* **Description:** Predict the estimated price of a software product.
* **Headers:** `Authorization: Bearer <API_KEY>`
* **Request Body:**

```json
{
  "name": "Your Name",
  "softwarename": "Software Name",
  "data": [2, 9, 40.0, 1, 0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 8.0],
  "currency": "USD"
}
```

* **Response:**

```json
{
  "prediction": 1234.56,
  "currency": "USD",
  "curency_price": 1234.56
}
```

---

### 2. **Admin Management** (Requires HTTP Basic Auth)

| Endpoint                     | Description                 |
| ---------------------------- | --------------------------- |
| `POST /admins/create`        | Create a new admin user.    |
| `GET /admins/get/{id}`       | Get admin user by ID.       |
| `GET /admins/email/{email}`  | Get admin user by email.    |
| `GET /admins/name/{name}`    | Get admin user by name.     |
| `PUT /admins/update/{id}`    | Update admin user details.  |
| `DELETE /admins/delete/{id}` | Delete an admin user by ID. |

**Authentication:** Basic Auth with credentials provided by OmniSoft.

---

### 3. **Token Management** (Requires HTTP Basic Auth)

| Endpoint                        | Description                    |
| ------------------------------- | ------------------------------ |
| `POST /tokens/create`           | Create a new token for a user. |
| `GET /tokens/get/{token}`       | Retrieve token details.        |
| `GET /tokens/verify/{token}`    | Verify if a token is valid.    |
| `DELETE /tokens/delete/{token}` | Delete a token.                |

**Authentication:** Basic Auth with admin credentials.

---

## How to Use

1. Obtain your API key from OmniSoft (free or paid plan).
2. Include it in your request headers:

```
Authorization: Bearer <API_KEY>
```

3. Make POST requests to `/ai/predict` to get software price predictions.

**Example Python usage:**

```python
import requests

url = "https://your-api-domain.com/ai/predict"
headers = {"Authorization": "Bearer YOUR_API_KEY"}
payload = {
    "name": "John Doe",
    "softwarename": "MyApp",
    "data": [2, 9, 40.0, 1, 0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 8.0],
    "currency": "USD"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

---

## License

MIT License – see [LICENSE](LICENSE) for details.

---

## Contact

**OmniSoft Limited**
Email: `omnisoft.ltd`
Website: [https://omnisoft.ltd](https://omnisoft.ltd)
