import { Row, Col } from "antd";
import WSCard from "./WSCard";

const WSGrid = ({ tables }) => {
  // Render a grid of WSCard components for the provided tables
  return (
    <Row gutter={[16, 16]}>
      {/* Map through the tables array to create a WSCard component for each table */}
      {tables.map((table) => (
        <Col key={table.tableId} xs={24} sm={12} md={10} lg={8}>
          {/* Pass the table object as a prop to the WSCard component */}
          <WSCard table={table} />
        </Col>
      ))}
    </Row>
  );
};

export default WSGrid;
