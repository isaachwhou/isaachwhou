import React from "react";
import { Carousel, Modal, Row, Col, Card } from "antd";
import { FaStar } from "react-icons/fa";
import { GiFire } from "react-icons/gi";
import { useState } from "react";
import CustomerDetailedDish from "./CustomerDetailedDish";

// Displays carousels of top-rated and top-selling dishes.
// It accepts topRatingDish, topSellingDish, tableId, orderId as props.
const CarouselComponent = ({
  topRatingDish,
  topSellingDish,
  tableId,
  orderId,
}) => {
  //State intial and trigger
  const [showDetail, setShowDetail] = useState(false);
  const [selectedDish, setSelectedDish] = useState(null);

  const displayDetail = (dish) => {
    setSelectedDish(dish);
    setShowDetail(true);
  };

  const handleCancelDisplayDetail = () => {
    setShowDetail(false);
  };

  return (
    <>
      {/* Top Rated Dishes Carousel */}
      <Row gutter={[18, 18]}>
        {/* Top Rated Dishes Carousel */}
        <Col xs={24} md={12}>
          <Card
            title={
              <h2
                style={{
                  fontFamily: "Lato",
                  fontWeight: "bold",
                  textAlign: "center",
                }}
              >
                <FaStar style={{ marginRight: 5 }} />
                Top Rated
              </h2>
            }
            bordered
            hoverable
          >
            {topRatingDish && topRatingDish.length > 0 ? (
              <Carousel
                style={{ width: "100%", maxWidth: "600px" }}
                autoplay
                dotPosition="bottom"
              >
                {topRatingDish.map((dish) => (
                  <div key={`rating_${dish.itemId}`}>
                    <img
                      src={`data:image/jpeg;base64,${dish.picture}`}
                      alt={dish.name}
                      style={{
                        width: "100%",
                        height: "300px",
                        cursor: "pointer",
                      }}
                      onClick={() => displayDetail(dish)}
                    />
                    <div
                      style={{
                        textAlign: "center",
                        fontFamily: "Lato",
                        fontSize: "16px",
                      }}
                    >
                      {dish.name}
                    </div>
                  </div>
                ))}
              </Carousel>
            ) : (
              <div>No top-rated dishes found.</div>
            )}
          </Card>
        </Col>

        {/* Top Selling Dishes Carousel */}
        <Col xs={24} md={12}>
          <Card
            title={
              <h2
                style={{
                  fontFamily: "Lato",
                  fontWeight: "bold",
                  textAlign: "center",
                }}
              >
                <GiFire style={{ marginRight: 5 }} />
                Best Seller
              </h2>
            }
            bordered
            hoverable
          >
            {topSellingDish && topSellingDish.length > 0 ? (
              <Carousel
                style={{ width: "100%", maxWidth: "600px" }}
                autoplay
                dotPosition="bottom"
              >
                {topSellingDish.map((dish) => (
                  <div key={`selling_${dish.itemId}`}>
                    <img
                      src={`data:image/jpeg;base64,${dish.picture}`}
                      alt={dish.name}
                      style={{
                        width: "100%",
                        height: "300px",
                        cursor: "pointer",
                      }}
                      onClick={() => displayDetail(dish)}
                    />
                    <div
                      style={{
                        textAlign: "center",
                        fontFamily: "Lato",
                        fontSize: "16px",
                      }}
                    >
                      {dish.name}
                    </div>
                  </div>
                ))}
              </Carousel>
            ) : (
              <div>No top-selling dishes found.</div>
            )}
          </Card>
        </Col>
      </Row>

      {/* Modal for displaying detailed dish */}
      {selectedDish && (
        <Modal
          open={showDetail}
          onCancel={handleCancelDisplayDetail}
          footer={null}
          destroyOnClose
          maskClosable
          closable
          centered
        >
          <CustomerDetailedDish
            itemId={selectedDish.itemId}
            tableId={tableId}
            orderId={orderId}
          />
        </Modal>
      )}
    </>
  );
};

export default CarouselComponent;
