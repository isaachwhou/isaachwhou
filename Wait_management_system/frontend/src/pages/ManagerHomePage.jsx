import { Layout, Button, Modal, Popconfirm, Space, message } from "antd";
import {
  DeleteTwoTone,
  LineChartOutlined,
  PlusOutlined,
} from "@ant-design/icons";
import { ReactSortable } from "react-sortablejs";
import { Link, Element } from "react-scroll";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";

import AddDishForm from "../components/manager/AddDishForm";
import AddCatForm from "../components/manager/AddCatForm";
import DishGrid from "../components/manager/DishGrid";
import "../App.css";

const { Header, Content, Sider } = Layout;

const ManagerHomePage = () => {
  const dragCatColor = {
    fontSize: "25px",
    color: "#2131231",
  };

  const navigate = useNavigate();
  const [addDishOpen, addDishSetOpen] = useState(false);
  const [addCatOpen, addCatSetOpen] = useState(false);
  const [Category, setCategory] = useState([]);
  const [Dishes, setDishes] = useState([]);
  const [delCat, delCatOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isSmallScreen, setIsSmallScreen] = useState(false);

  // fetch data and render again after adding new categories and dishes.
  React.useEffect(() => {
    fetchCategory();
    console.log("fetching category");
  }, [addCatOpen,delCat]);

  React.useEffect(() => {
    fetchAllDishes();
    console.log(addDishOpen, "fetching dishes");
  }, [addDishOpen]);

  // trigger func for delete alarm.
  const showDelCat = () => {
    console.log("Del Cat");
    delCatOpen(true);
  };

  // Build cateogry moving structure.
  const buildMap = (keys, values) => {
    const map = new Map();
    for (let i = 0; i < keys.length; i++) {
      map.set(keys[i], values[i]);
    }
    return map;
  };

  // post changed order to backend.
  const fetchCatSeq = (data) => {
    //console.log(data)
    var catNameList = ([] = data.map((item) => {
      return item.categoryId;
    }));
    var catOrderList = ([] = data.map((item) => {
      return item.index;
    }));
    //console.log(catNameList);
    //console.log(catOrderList);
    const newMap = buildMap(catNameList, catOrderList.sort());
    const obj = Object.fromEntries(newMap);
    const json = JSON.stringify(obj);
    console.log(json);
    fetch(`http://localhost:8080/waitsys/manager/change_category_order`, {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: json,
    })
      .then((response) => {
        if (response.status === 200) {
          console.log("Success:", response);
        } else {
          throw new Error("Failed to move dish.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  // Fetch category
  const fetchCategory = async () => {
    try {
      const response = await fetch(
        "http://localhost:8080/waitsys/manager/list_all_categories",
        {
          method: "GET",
          headers: {
            "Content-type": "application/json",
          },
        }
      );
      const data = await response.json();
      const processedData = data.map((item) => ({
        categoryId: item.id,
        name: item.name,
        index: item.orderNum,
      }));
      setCategory(processedData);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // click and nav to stat page.
  const goStatisticsPage = () => {
    const targetUrl = "/statistics";
    console.log("Go to statistics page");
    navigate(targetUrl);
  };

  // get all dishes information
  const fetchAllDishes = async () => {
    try {
      const response = await fetch(
        "http://localhost:8080/waitsys/manager/item/showAll?pageNo=1&pageSize=10",
        {
          method: "GET",
          headers: {
            "Content-type": "application/json",
          },
        }
      );
      const data = await response.json();
      const processedData = data.records.map((item) => ({
        itemId: item.itemId,
        name: item.name,
        picture: item.picture,
        description: item.description,
        ingredient: item.ingredient,
        price: item.price,
        categoryId: item.categoryId,
        rating: item.rating,
        isOnMenu: item.isOnMenu,
        orderNum: item.orderNum,
        category: item.category,
      }));
      setDishes(processedData);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // delete category and synchronize to backend.
  const DeleteCategory = (categoryId) => {
    const formData = new FormData();
    formData.append("itemId", categoryId);
    fetch(
      `http://localhost:8080/waitsys/manager/remove_category?id=${categoryId}`,
      {
        method: "POST",
      }
    )
      .then((response) => {
        if (response.status === 200) {
          console.log("Delete success:", response);
          message.success("Dish deleted successfully!");
          fetchCategory();
        } else {
          throw new Error("Failed to delete dish.");
        }
      })
      .catch((error) => {
        console.error("Delete failed:", error);
      });
  };

  const addTableHandler = () => {
    // Make a POST request to add a table to the backend
    fetch("http://localhost:8080/waitsys/customer/table/addTable", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          console.log("Table added successfully!");
          // Fetch the total number of tables to display the message
          fetch("http://localhost:8080/waitsys/customer/table/getTableNum")
            .then((response) => response.text()) // Use response.text() instead of response.json()
            .then((totalTables) => {
              if (totalTables === "") {
                throw new Error("Total tables is undefined.");
              }
              message.success(
                `Table added successfully! Total tables: ${totalTables}`
              );
            })
            .catch((error) => {
              console.error("Error while fetching table data:", error);
            });
        } else {
          throw new Error("Failed to add a table.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  // triggers for states changing.
  const showAddDish = () => {
    console.log("Add Dish");
    addDishSetOpen(true);
  };

  const handleCancelAddDish = () => {
    console.log("Cancel Add Dish");
    addDishSetOpen(false);
  };

  const showAddCat = () => {
    console.log("Add Cat");
    addCatSetOpen(true);
  };

  const handleCancelAddCat = () => {
    console.log("Cancel Add Cat");
    addCatSetOpen(false);
  };

  const confirm = (categoryId) => {
    DeleteCategory(categoryId);
  };

  const cancel = (e) => {
    console.log(e);
  };

  const handleBreakpoint = (broken) => {
    setIsSmallScreen(broken);
  };

  const handleCollapse = (collapsed, type) => {
    setIsCollapsed(collapsed);
  };

  return (
    <Layout hasSider>
      <Sider
        theme="light"
        style={{
          overflow: "auto",
          height: "100vh",
          position: "fixed",
          left: 0,
          top: 0,
          bottom: 0,
          boxShadow: "4px 0 8px rgba(0, 0, 0, 0.1)",
        }}
        breakpoint="lg"
        collapsedWidth="0"
        onBreakpoint={handleBreakpoint}
        onCollapse={handleCollapse}
      >
        <div className="lato-bold" style={{ margin: "32px 25px" }}>
          Menu
        </div>
        <ReactSortable
          style={dragCatColor}
          list={Category}
          setList={setCategory}
          onChange={fetchCatSeq(Category)}
        >
          {Category.map((item, index) => (
            <div
              className="draggableItem"
              key={`category${index}`}
              style={{
                margin: "28px 25px",
              }}
            >
              <Link
                activeClass="active"
                className={item.name}
                to={item.name}
                spy={true}
                smooth={true}
                duration={500}
              ></Link>
              <div className="category-container">{item.name}</div>
              <Popconfirm
                title="Delete the task"
                description="Are you sure to delete this task?"
                onConfirm={() => confirm(item.categoryId)}
                onCancel={cancel}
              >
                <Button icon={<DeleteTwoTone />} onClick={showDelCat} />
              </Popconfirm>
            </div>
          ))}
        </ReactSortable>
      </Sider>
      <Layout style={{ marginLeft: isSmallScreen ? 0 : 200 }}>
        <Header
          style={{
            background: "#fff",
            color: "#333",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            marginLeft: -10,
            marginTop: -10,
            boxShadow: "2px 5px 12px rgba(0, 0, 0, 0.1)",
          }}
        >
          <div className="lato">
            <h1>Manager Page</h1>
          </div>
        </Header>
        <Content style={{ margin: "12px 16px", overflow: "initial" }}>
          <Space size={12}>
            <Button icon={<PlusOutlined />} onClick={showAddDish}>
              Add New Dish
            </Button>
            <Button icon={<PlusOutlined />} onClick={showAddCat}>
              Add New Category
            </Button>
            <Button icon={<PlusOutlined />} onClick={addTableHandler}>
              Add Table
            </Button>
            <Button onClick={goStatisticsPage} icon={<LineChartOutlined />}>
              Statistics
            </Button>
          </Space>
          <Modal
            open={addDishOpen}
            onCancel={handleCancelAddDish}
            footer={null}
            keyboard
          >
            <AddDishForm onClose={handleCancelAddDish} />
          </Modal>
          <Modal
            open={addCatOpen}
            onCancel={handleCancelAddCat}
            footer={null}
            keyboard
          >
            <AddCatForm onClose={handleCancelAddCat} />
          </Modal>
          {Category.map((item) => (
            <div key={item.categoryId} id={`grid${item.name}`}>
              <Element name={item.name} className="lato-small">
                <h2>{item.name}</h2>
              </Element>
              <DishGrid categoryId={item.categoryId} AllDish={Dishes} />
            </div>
          ))}
        </Content>
      </Layout>
    </Layout>
  );
};
export default ManagerHomePage;
