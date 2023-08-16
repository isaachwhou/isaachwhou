import * as React from "react";
import { useState, useEffect } from "react";
import { PlusOutlined } from "@ant-design/icons";
import { Button, Form, Input, InputNumber, Upload, Card, Space, message, Select } from "antd";

const { Option } = Select;

const normFile = (e) => {
  if (Array.isArray(e)) {
    return e;
  }
  return e?.fileList;
};

const ModifyDishForm = ({ onClose, itemId }) => {
  const [file, setFile] = useState(null);
  const [categories, setCategories] = useState([]);
  const [item, setItem] = useState(null);

  useEffect(() => {
    fetchCategories();
    fetchItem();
  }, []);

  const fetchCategories = () => {
    fetch("http://localhost:8080/waitsys/manager/list_all_categories")
      .then((response) => response.json())
      .then((data) => {
        setCategories(data);
      })
      .catch((error) => {
        console.log("Error fetching categories:", error);
      });
  };

  const fetchItem = async () => {
    try {
      const response = await fetch(
        `http://localhost:8080/waitsys/manager/item/showById?itemId=${itemId}`,
        {
          method: "GET",
          headers: {
            "Content-type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error("Failed to fetch item");
      }
      const data = await response.json();
      console.log("Fetched item data:", data);
      const processedData = {
        title: data.name,
        price: data.price,
        id: data.itemId,
        description: data.description,
        ingredient: data.ingredient,
        categoryId: data.categoryId,
        picture: `data:image/jpeg;base64, ${data.picture}`,
        pictureonly: data.picture,
      };
      console.log("Processed item data:", processedData);
      setItem(processedData);
    } catch (error) {
      console.log("Error fetching item:", error);
    }
  };

  const onFinish = (values) => {
    const formData = new FormData();
    formData.append("itemId", itemId);
    formData.append("name", values.dishName);
    formData.append("description", values.description);
    formData.append("ingredient", values.ingredients);
    formData.append("price", values.price);
    formData.append("categoryId", values.dishCategory);
    if (file) {
      formData.append("picture", file);
    } else {
      formData.append("picture", base64ToFile(item.pictureonly));
    }
    sendFormData(formData);
  };

  const base64ToFile = (base64Data) => {
    const byteCharacters = atob(base64Data);
    const byteArrays = [];
    for (let i = 0; i < byteCharacters.length; i++) {
      byteArrays.push(byteCharacters.charCodeAt(i));
    }
    const byteArray = new Uint8Array(byteArrays);
    return new File([byteArray], "picture.jpg", { type: "image/jpeg" });
  };

  const sendFormData = (data) => {
    fetch("http://localhost:8080/waitsys/manager/item/edit", {
      method: "POST",
      body: data,
    })
      .then((response) => {
        if (response.status === 200) {
          console.log("Modify success:", response);
          message.success("Dish modified successfully!");
          onClose();
          window.location.reload();
        } else {
          throw new Error("Failed to modify dish.");
        }
      })
      .catch((error) => {
        console.error("Modify failed:", error);
      });
  };

  // post delete command to the backend.
  const handleDelete = () => {
    const formData = new FormData();
    formData.append("itemId", itemId);
    fetch(`http://localhost:8080/waitsys/manager/item/delete?itemId=${itemId}`, {
      method: "GET",
    })
      .then((response) => {
        if (response.status === 200) {
          console.log("Delete success:", response);
          message.success("Dish deleted successfully!");
          onClose();
          window.location.reload();
        } else {
          throw new Error("Failed to delete dish.");
        }
      })
      .catch((error) => {
        console.error("Delete failed:", error);
      });
  };

  const beforeUpload = (file) => {
    const allowedTypes = ["image/jpeg", "image/png"];
    const isAllowed = allowedTypes.includes(file.type);
    if (!isAllowed) {
      console.log("Only JPG/PNG files are allowed!");
    } else {
      setFile(file); // Update the image file state variable
    }
    return false; // Returning false prevents immediate upload
  };

  // image validation
  const uploadProps = {
    beforeUpload,
    maxCount: 1,
    listType: "picture-card",
    accept: "image/jpeg, image/png",
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  if (!item) {
    return null; 
  }

  return (
    // Use form to collect information.
    // And pre existed information will be filling in to blank first.
    // Manager can change as there wishes.
    // Only MODIFY or DELETE button will trigger the changes.
    <Card title="Modify Dish" name="modifyDishForm" bordered={false}>
      <Form
        name="basic"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 20,
        }}
        initialValues={{
          dishName: item.title,
          price: item.price,
          description: item.description,
          ingredients: item.ingredient,
          dishCategory: item.categoryId,
        }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
      >
        <Form.Item
          label="Dish Image"
          valuePropName="fileList"
          getValueFromEvent={normFile}
        >
          <Upload
            {...uploadProps}
            action="/upload.do"
            listType="picture-card"
            beforeUpload={beforeUpload}
            defaultFileList={item.picture ? [{ uid: '1', name: 'image', status: 'done', url: item.picture }] : []}
          >
            <div>
              <PlusOutlined />
              <div
                style={{
                  marginTop: 8,
                  alignItems: "center",
                }}
              >
                Upload
              </div>
            </div>
          </Upload>
        </Form.Item>
        <Form.Item
          label="Dish Name"
          name="dishName"
          rules={[
            {
              required: true,
              message: "Please input the name of the dish!",
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="Price"
          name="price"
          rules={[
            {
              required: true,
              message: "Please input the price of the dish!",
            },
          ]}
        >
          <InputNumber />
        </Form.Item>
        <Form.Item
          label="Description"
          name="description"
          rules={[
            {
              required: true,
              message: "Please input the description of the dish!",
            },
          ]}
        >
          <Input.TextArea />
        </Form.Item>
        <Form.Item
          label="Ingredients"
          name="ingredients"
          rules={[
            {
              required: true,
              message: "Please input the ingredient of the dish!",
            },
          ]}
        >
          <Input.TextArea />
        </Form.Item>
        <Form.Item
        label="Category"
        name="dishCategory"
        rules={[
          {
            required: true,
            message: "Please select the category!",
          },
        ]}
      >
        <Select>
          {categories.map((category) => (
            <Option key={category.name} value={category.id}>
              {category.name}
            </Option>
          ))}
        </Select>
        </Form.Item>
        <Form.Item
          wrapperCol={{
            offset: 5,
            span: 16,
          }}
        >
          <Space size={20}>
            <Button
              type="primary"
              shape="round"
              htmlType="submit"
              style={{ backgroundColor: "green" }}
            >
              Modify
            </Button>
            <Button type="primary" danger onClick={handleDelete}>
              Delete
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default ModifyDishForm;