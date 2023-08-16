import * as React from "react";
import { useState } from "react";
import { PlusOutlined } from "@ant-design/icons";
import {
  Button,
  Form,
  Input,
  InputNumber,
  Upload,
  Card,
  message,
  Select,
} from "antd";

const { Option } = Select;


const normFile = (e) => {
  if (Array.isArray(e)) {
    return e;
  }
  return e?.fileList;
};

// Add dish function.
// manager can only add new dish when all infor are input.
const AddDishForm = ({ onClose }) => {
  const [file, setFile] = useState(null); 
  const [categories, setCategories] = useState([]);
  const [form] = Form.useForm();

  React.useEffect(() => {
    fetchCategories();
  }, []);

  // using on dropdown selection.
  // help manager to choose which category new dish belongs to.
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

  // formatting the input data and do the validation.
  const onFinish = async (values) => {
    const formData = new FormData();
    formData.append("name", values.dishName);
    formData.append("description", values.description);
    formData.append("ingredient", values.ingredients);
    formData.append("price", values.price);
    formData.append("categoryId", values.dishCategory);
    if (file) {
      formData.append("picture", file);
    } else {
      message.error("Please add dish image.");
      return;
    }
    await sendFormData(formData);
    form.resetFields();
    form.resetFields(["dishImage"]);
  };

  // send data to backend. Expected create dish successfully.
  const sendFormData = async (data) => {
    fetch("http://localhost:8080/waitsys/manager/item/add", {
      method: "POST",
      body: data,
    })
      .then((response) => {
        console.log(response);
        if (response.status === 200) {
          message.success("Dish added successfully!");
          onClose();
        } else {
          throw new Error("Error adding dish");
        }
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  };

  // image validation.
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

  const uploadProps = {
    beforeUpload,
    maxCount: 1,
    listType: "picture-card",
    accept: "image/jpeg, image/png",
  };

  return (
    <Card title="Add New Dish" name="addDishCard" bordered={false}>
      <Form
        form={form}
        name="addDishForm"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 20,
        }}
        initialValues={{
          remember: true,
        }}
        onFinish={onFinish}
      >
        <Form.Item
          label="Dish Image"
          name="dishImage"
          valuePropName="fileList"
          getValueFromEvent={normFile}
        >
          <Upload
            {...uploadProps}
            action="/upload.do"
            listType="picture-card"
            beforeUpload={beforeUpload}
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
          wrapperCol={{
            offset: 8,
            span: 16,
          }}
        >
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default AddDishForm;