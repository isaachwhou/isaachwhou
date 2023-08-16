import { Card, Divider, Modal, Rate, Tag } from "antd";
import CustomerDetailedDish from "./CustomerDetailedDish";
import { useState } from "react";
import * as React from "react";
const { Meta } = Card;

// the dish card components. will be called by dish grid.
const CustomerDishCard = ({
  ItemId,
  title,
  price,
  picture,
  tableId,
  orderId,
  itemRate,
}) => {
  const [showDetail, updateShowDetail] = useState(false);

  const displayDetail = () => {
    updateShowDetail(true);
  };

  // handle cancel Display detail dishcard.
  const handleCancelDisplayDetail = () => {
    setTimeout(() => {
      updateShowDetail(false);
    }, 0);
  };

  // initial the item rate.
  const isItemRatedZero = itemRate === 0;

  return (
    // display all information by card.
    // click will trigger show detailed dish card.
    // click the mask will close the detailed dish card.
    <Card
      cover={
        <img alt="image" src={picture} style={{ width: "100%", height: 200 }} />
      }
      hoverable={true}
      onClick={displayDetail}
    >
      <Modal
        open={showDetail}
        onCancel={handleCancelDisplayDetail}
        footer={null}
        destroyOnClose={true}
        maskClosable={true}
        closable={true}
        centered={true}
      >
        <CustomerDetailedDish
          itemId={ItemId}
          tableId={tableId}
          orderId={orderId}
        />
      </Modal>
      <Meta title={title} description={"$" + price} />
      <Divider />
      <div>
        {//find if there are any previous rate for this dish.
        }
        {isItemRatedZero ? (
          <div style={{ display: "flex", alignItems: "center" }}>
            <Tag
              style={{ height: 30, lineHeight: `30px`, marginBottom: 0 }}
              color="blue"
            >
              No Rating
            </Tag>
          </div>
        ) : (
          <div style={{ display: "flex", alignItems: "center" }}>
            <Rate
              disabled
              defaultValue={itemRate}
              style={{ height: 30, lineHeight: "30px", marginBottom: 0 }}
            />
          </div>
        )}
      </div>
    </Card>
  );
};

export default CustomerDishCard;
