import { useEffect, useState } from "react";
import { Layout, Typography } from "antd";
import WSGrid from "../components/waitstaff/WSGrid";

const { Header, Content } = Layout;
const { Title } = Typography;

const WaitStaffHomePage = () => {
  // State to hold the list of tables
  const [tables, setTables] = useState([]);

  // Fetch the tables data from the server and update the state
  useEffect(() => {
    fetchTables();
    const timer = setInterval(fetchTables, 1000);
    // Cleanup function to clear the interval when the component is unmounted
    return () => clearInterval(timer);
  }, []);

  // Function to fetch tables data from the server
  const fetchTables = async () => {
    try {
      const response = await fetch(
        "http://localhost:8080/waitsys/waitstaff/list_all_tables_waitstaff"
      );
      const data = await response.json();
      setTables(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // Render the Wait Staff Home Page layout
  return (
    <Layout>
      {/* Header section */}
      <Header style={{ background: "#ffffff" }}>
        <Title level={3} style={{ color: "black", textAlign: "center", fontFamily: "Lato, sans-serif", fontWeight: "bold",}}>
          Wait Staff Home Page
        </Title>
      </Header>
      {/* Content section */}
      <Content style={{ margin: "24px 16px 0", overflow: "initial" }}>
        {/* Render the WSGrid component and pass the tables data as a prop */}
        <WSGrid tables={tables} />
      </Content>
    </Layout>
  );
};

export default WaitStaffHomePage;
