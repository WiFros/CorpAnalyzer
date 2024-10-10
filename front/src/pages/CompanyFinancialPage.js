import React, { useEffect, useState, useCallback, useRef } from "react";
import { useLocation } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import { Line, Doughnut, Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from 'chart.js';
import { Card, CardHeader, CardBody, Divider } from "@nextui-org/react";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

const CompanyFinancialPage = () => {
    const location = useLocation();
    const company = location.state?.company;

    const [financialData, setFinancialData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchedRef = useRef(false);

    const fetchFinancialData = useCallback(async () => {
        if (!company || fetchedRef.current) return;

        setIsLoading(true);
        setError(null);
        try {
            const response = await axiosInstance.get(`/api/companies/financials/${encodeURIComponent(company.company_name)}`);
            setFinancialData(response.data.financial_data);
            fetchedRef.current = true;
        } catch (err) {
            console.error("Failed to fetch financial data:", err.response ? err.response.data : err.message);
            setError("재무 데이터를 불러오는 중 오류가 발생했습니다.");
        } finally {
            setIsLoading(false);
        }
    }, [company]);

    useEffect(() => {
        fetchFinancialData();
    }, [fetchFinancialData]);

    if (isLoading) return <div>로딩 중...</div>;
    if (error) return <div>{error}</div>;
    if (!financialData) return <div>{company?.company_name}의 재무 데이터를 사용할 수 없습니다.</div>;

    const years = Object.keys(financialData).sort();

    // 억 원 단위로 변환하는 함수
    const convertToBillions = (value) => {
        return value / 100000000;
    };


    // 1. 주요 재무 지표 계산
    const calculateGrowthRate = (current, previous) => ((current - previous) / previous) * 100;

    const salesGrowth = years.map((year, index) => {
        if (index === 0) return 0;
        const currentSales = Number(financialData[year].financials["매출액"].replace(/,/g, ""));
        const previousSales = Number(financialData[years[index-1]].financials["매출액"].replace(/,/g, ""));
        return calculateGrowthRate(currentSales, previousSales);
    });

    const operatingMargin = years.map(year => {
        const sales = Number(financialData[year].financials["매출액"].replace(/,/g, ""));
        const operatingProfit = Number(financialData[year].financials["영업이익"].replace(/,/g, ""));
        return (operatingProfit / sales) * 100;
    });

    const netProfitMargin = years.map(year => {
        const sales = Number(financialData[year].financials["매출액"].replace(/,/g, ""));
        const netProfit = Number(financialData[year].financials["당기순이익"].replace(/,/g, ""));
        return (netProfit / sales) * 100;
    });

    const assetGrowth = years.map((year, index) => {
        if (index === 0) return 0;
        const currentAssets = Number(financialData[year].financials["자산총계"].replace(/,/g, ""));
        const previousAssets = Number(financialData[years[index-1]].financials["자산총계"].replace(/,/g, ""));
        return calculateGrowthRate(currentAssets, previousAssets);
    });

    // 2. 재무 건전성 지표
    const debtRatio = years.map(year => {
        const totalLiabilities = Number(financialData[year].financials["부채총계"].replace(/,/g, ""));
        const totalEquity = Number(financialData[year].financials["자본총계"].replace(/,/g, ""));
        return (totalLiabilities / totalEquity) * 100;
    });

    const currentRatio = years.map(year => {
        const currentAssets = Number(financialData[year].financials["유동자산"].replace(/,/g, ""));
        const currentLiabilities = Number(financialData[year].financials["유동부채"].replace(/,/g, ""));
        return (currentAssets / currentLiabilities) * 100;
    });

    // 3. 수익성 지표
    const ROE = years.map(year => {
        const netIncome = Number(financialData[year].financials["당기순이익"].replace(/,/g, ""));
        const equity = Number(financialData[year].financials["자본총계"].replace(/,/g, ""));
        return (netIncome / equity) * 100;
    });

    const ROA = years.map(year => {
        const netIncome = Number(financialData[year].financials["당기순이익"].replace(/,/g, ""));
        const assets = Number(financialData[year].financials["자산총계"].replace(/,/g, ""));
        return (netIncome / assets) * 100;
    });

    // 4. 자산 구조 분석
    const assetStructure = years.map(year => {
        const currentAssets = Number(financialData[year].financials["유동자산"].replace(/,/g, ""));
        const nonCurrentAssets = Number(financialData[year].financials["비유동자산"].replace(/,/g, ""));
        const totalAssets = currentAssets + nonCurrentAssets;
        return {
            year,
            currentAssetsRatio: (currentAssets / totalAssets) * 100,
            nonCurrentAssetsRatio: (nonCurrentAssets / totalAssets) * 100
        };
    });

    // 차트 데이터 구성
    const salesData = {
        labels: years,
        datasets: [
            {
                label: "매출액 (억원)",
                data: years.map(year => convertToBillions(Number(financialData[year].financials["매출액"].replace(/,/g, "")))),
                borderColor: "rgba(75, 192, 192, 1)",
                fill: false,
            },
            {
                label: "매출 성장률",
                data: salesGrowth,
                borderColor: "rgba(255, 99, 132, 1)",
                fill: false,
                yAxisID: 'y1',
            }
        ],
    };

    const profitabilityData = {
        labels: years,
        datasets: [
            {
                label: "영업이익률",
                data: operatingMargin,
                borderColor: "rgba(75, 192, 192, 1)",
                fill: false,
            },
            {
                label: "순이익률",
                data: netProfitMargin,
                borderColor: "rgba(255, 99, 132, 1)",
                fill: false,
            }
        ],
    };

    const healthData = {
        labels: years,
        datasets: [
            {
                label: "부채비율",
                data: debtRatio,
                borderColor: "rgba(75, 192, 192, 1)",
                fill: false,
            },
            {
                label: "유동비율",
                data: currentRatio,
                borderColor: "rgba(255, 99, 132, 1)",
                fill: false,
            }
        ],
    };

    const profitabilityRatiosData = {
        labels: years,
        datasets: [
            {
                label: "ROE",
                data: ROE,
                borderColor: "rgba(75, 192, 192, 1)",
                fill: false,
            },
            {
                label: "ROA",
                data: ROA,
                borderColor: "rgba(255, 99, 132, 1)",
                fill: false,
            }
        ],
    };

    const assetStructureData = {
        labels: years,
        datasets: [
            {
                label: "유동자산 비율",
                data: assetStructure.map(item => item.currentAssetsRatio),
                backgroundColor: "rgba(75, 192, 192, 0.5)",
            },
            {
                label: "비유동자산 비율",
                data: assetStructure.map(item => item.nonCurrentAssetsRatio),
                backgroundColor: "rgba(255, 99, 132, 0.5)",
            }
        ],
    };

    return (
        <div className="p-8" style={{ paddingTop: "100px", textAlign: "center" }}>
            <h1 className="text-3xl font-bold mb-4 font-kopub">{company.company_name} 재무제표 분석</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="w-full">
                    <CardHeader className="font-bold">매출액 및 성장률 추이</CardHeader>
                    <Divider />
                    <CardBody>
                        <Line
                            data={salesData}
                            options={{
                                scales: {
                                    y: {
                                        type: 'linear',
                                        display: true,
                                        position: 'left',
                                    },
                                    y1: {
                                        type: 'linear',
                                        display: true,
                                        position: 'right',
                                        grid: {
                                            drawOnChartArea: false,
                                        },
                                    },
                                }
                            }}
                        />
                    </CardBody>
                </Card>

                <Card className="w-full">
                    <CardHeader className="font-bold">수익성 지표</CardHeader>
                    <Divider />
                    <CardBody>
                        <Line data={profitabilityData} />
                    </CardBody>
                </Card>

                <Card className="w-full">
                    <CardHeader className="font-bold">재무 건전성 지표</CardHeader>
                    <Divider />
                    <CardBody>
                        <Line data={healthData} />
                    </CardBody>
                </Card>

                <Card className="w-full">
                    <CardHeader className="font-bold">수익성 비율 (ROE & ROA)</CardHeader>
                    <Divider />
                    <CardBody>
                        <Line data={profitabilityRatiosData} />
                    </CardBody>
                </Card>
            </div>

            <div className="mt-4">
                <Card className="w-full">
                    <CardHeader className="font-bold">자산 구조 분석</CardHeader>
                    <Divider />
                    <CardBody>
                        <Bar data={assetStructureData} options={{ scales: { x: { stacked: true }, y: { stacked: true } } }} />
                    </CardBody>
                </Card>
            </div>
        </div>
    );
};

export default CompanyFinancialPage;