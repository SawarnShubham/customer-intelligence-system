-- =========================================================
-- Customer Intelligence & Revenue Optimization System
-- SQL Business Analysis Queries
--
-- Purpose:
-- These queries help identify high-value customers,
-- revenue trends, repeat buyers, and business growth opportunities.
--
-- Table Used:
-- cleaned_data
--
-- Main Columns:
-- CustomerID
-- InvoiceNo
-- InvoiceDate
-- Country
-- Quantity
-- UnitPrice
-- TotalPrice
-- =========================================================


-- =========================================================
-- Query 1: Top 10 Customers by Revenue
--
-- Business Question:
-- Which customers generate the highest revenue?
--
-- Business Impact:
-- Helps identify VIP customers for retention strategies,
-- loyalty rewards, and premium customer support.
-- =========================================================

SELECT
    CustomerID,
    SUM(TotalPrice) AS TotalRevenue
FROM cleaned_data
GROUP BY CustomerID
ORDER BY TotalRevenue DESC
LIMIT 10;


-- =========================================================
-- Query 2: Monthly Revenue Trend
--
-- Business Question:
-- Is revenue increasing or decreasing over time?
--
-- Business Impact:
-- Helps identify seasonal sales patterns,
-- weak months, and high-performing periods
-- for better inventory and marketing planning.
-- =========================================================

SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS Month,
    SUM(TotalPrice) AS Revenue
FROM cleaned_data
WHERE InvoiceDate IS NOT NULL
AND InvoiceDate != '0000-00-00'
GROUP BY Month
ORDER BY Month;


-- =========================================================
-- Query 3: Top 10 Countries by Revenue
--
-- Business Question:
-- Which countries generate the most revenue?
--
-- Business Impact:
-- Helps in expansion planning, regional marketing,
-- and shipping optimization decisions.
-- =========================================================

SELECT
    Country,
    SUM(TotalPrice) AS Revenue
FROM cleaned_data
GROUP BY Country
ORDER BY Revenue DESC
LIMIT 10;


-- =========================================================
-- Query 4: Repeat Customers
--
-- Business Question:
-- Which customers place multiple orders?
--
-- Business Impact:
-- Helps evaluate customer retention and
-- customer loyalty performance.
-- =========================================================

SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS TotalOrders
FROM cleaned_data
GROUP BY CustomerID
HAVING TotalOrders > 1
ORDER BY TotalOrders DESC
LIMIT 200;


-- =========================================================
-- Query 5: High-Value Customers Above Average Spend
--
-- Business Question:
-- Which customers spend more than the average customer?
--
-- Business Impact:
-- Helps create VIP customer groups,
-- premium campaigns, and personalized offers.
-- =========================================================

SELECT
    CustomerID,
    SUM(TotalPrice) AS Revenue
FROM cleaned_data
GROUP BY CustomerID
HAVING Revenue > (
    SELECT AVG(customer_total)
    FROM (
        SELECT
            CustomerID,
            SUM(TotalPrice) AS customer_total
        FROM cleaned_data
        GROUP BY CustomerID
    ) AS avg_table
)
ORDER BY Revenue DESC;