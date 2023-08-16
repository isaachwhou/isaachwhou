import { Card, Row, Col } from "antd";
import * as React from "react";
import DishCard from "./DishCard";
import { ReactSortable } from "react-sortablejs";
const { Meta } = Card;

// Same as customer dish grid
// feature: drag dish card and placed it in other position (within same category)
// it will reorder automatically in backend.
const GridList = ({ categoryId, AllDish }) => {
  const [dishes, setDishes] = React.useState([]);

  // if things changed, fetch data and render again.
  React.useEffect(() => {
    fetchData(categoryId);
    console.log("upate!!!!");
  }, [categoryId, AllDish]);

  // arrange new order of items after moving, and save it as state, trigger re-render.
  const handleChange = (event) => {
    const newDishes = [...dishes];
    const movedItem = newDishes.splice(event.oldIndex, 1)[0];
    newDishes.splice(event.newIndex, 0, movedItem);

    const dishUpdates = newDishes.map((dish, index) => {
      const newOrderNum = newDishes.length - index;
      return { id: dish.id, orderNum: newOrderNum };
    });

    dishUpdates.forEach(async (update) => {
      try {
        const response = await fetchMoveDish(update.id, update.orderNum);
        if (response.ok) {
          const dish = newDishes.find((d) => d.id === update.id);
          if (dish) {
            dish.orderNum = update.orderNum;
          }
        } else {
          throw new Error("Failed to update orderNum");
        }
      } catch (error) {
        console.error(error);
      }
    });
    setDishes(newDishes);
  };

  // post moved menu into backend
  const fetchMoveDish = async (dishId, newIndex) => {
    try {
      const response = await fetch(
        "http://localhost:8080/waitsys/manager/item/changeOrder",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ [dishId]: newIndex }),
        }
      );
      return response;
    } catch (error) {
      console.error(`Error: ${error}`);
    }
  };

  const fetchData = async (categoryId) => {
    try {
      const response = await fetch(
        `http://localhost:8080/waitsys/manager/item/showByCategory?categoryId=${categoryId}&pageNo=1&pageSize=99`,
        {
          method: "GET",
          headers: {
            "Content-type": "application/json",
          },
        }
      );
      const data = await response.json();
      const processedData = data.records.map((item) => ({
        title: item.name,
        price: item.price,
        index: item.orderNum,
        id: item.itemId,
        picture: `data:image/jpeg;base64, ${item.picture}`,
        rating: item.rating,
      }));
      setDishes(processedData);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <ReactSortable
      list={dishes}
      setList={setDishes}
      tag={Row}
      onUpdate={handleChange}
    >
      {dishes.map((dish) => (
        <Col key={dish.id} xs={24} sm={12} md={8} lg={6}>
          <div style={{ margin: "24px" }}>
            <DishCard
              title={dish.title}
              price={dish.price}
              index={dish.index}
              ItemId={dish.id}
              picture={dish.picture}
              itemRate={dish.rating}
            />
          </div>
        </Col>
      ))}
    </ReactSortable>
  );
};

export default GridList;
