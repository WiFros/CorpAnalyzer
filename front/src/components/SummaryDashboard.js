import React from 'react';
import { Card, CardHeader, CardBody, Divider } from "@nextui-org/react";
import { TrendingUp, TrendingDown, Minus, DollarSign, PieChart, BarChart2, Percent } from "lucide-react";

const SummaryDashboard = ({ financialData }) => {
    const latestYear = Object.keys(financialData).sort().pop();
    const previousYear = Object.keys(financialData).sort().slice(-2)[0];
    const latestData = financialData[latestYear].financials;
    const previousData = financialData[previousYear]?.financials;

    const formatNumber = (num) => {
        return new Intl.NumberFormat('ko-KR', {
            style: 'currency',
            currency: 'KRW',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(num / 100000000); // Convert to billions
    };

    const calculateRatio = (numerator, denominator) => {
        return ((Number(numerator.replace(/,/g, "")) / Number(denominator.replace(/,/g, ""))) * 100).toFixed(2);
    };

    const getColorClass = (value) => {
        const num = parseFloat(value.replace(/[^0-9.-]+/g, ""));
        return num < 0 ? "text-blue-600" : "text-red-600";
    };

    const calculateGrowth = (current, previous) => {
        if (!previous) return null;
        const growth = ((Number(current.replace(/,/g, "")) - Number(previous.replace(/,/g, ""))) / Number(previous.replace(/,/g, ""))) * 100;
        return growth.toFixed(2);
    };

    const renderTrendIcon = (growth) => {
        if (growth > 0) return <TrendingUp size={16} className="text-red-600" />;
        if (growth < 0) return <TrendingDown size={16} className="text-blue-600" />;
        return <Minus size={16} className="text-gray-600" />;
    };

    const getGrowthColorClass = (growth) => {
        if (parseFloat(growth) > 0) return "text-red-600";
        if (parseFloat(growth) < 0) return "text-blue-600";
        return "text-gray-600";
    };

    const renderMetricCard = (title, value, icon, prevValue) => {
        const growth = calculateGrowth(value, prevValue);
        const colorClass = getColorClass(value);

        return (
            <Card className="bg-gradient-to-br from-white to-gray-100 shadow-lg">
                <CardBody>
                    <div className="flex items-center justify-between mb-2">
                        <p className="text-sm font-semibold text-gray-600">{title}</p>
                        {React.createElement(icon, { size: 20, className: "text-gray-400" })}
                    </div>
                    <p className={`text-xl font-bold ${colorClass}`}>
                        {formatNumber(value.replace(/,/g, ""))}억원
                    </p>
                    {growth !== null && (
                        <div className="flex items-center mt-2">
                            {renderTrendIcon(parseFloat(growth))}
                            <span className={`text-xs ml-1 ${getGrowthColorClass(growth)}`}>
                                {Math.abs(parseFloat(growth)).toFixed(2)}% vs 전년
                            </span>
                        </div>
                    )}
                </CardBody>
            </Card>
        );
    };

    const renderRatioCard = (title, value, prevValue) => {
        const growth = calculateGrowth(value, prevValue);
        const colorClass = getColorClass(value);

        return (
            <Card className="bg-gradient-to-br from-white to-gray-100 shadow-lg">
                <CardBody>
                    <div className="flex items-center justify-between mb-2">
                        <p className="text-sm font-semibold text-gray-600">{title}</p>
                        <Percent size={20} className="text-gray-400" />
                    </div>
                    <p className={`text-xl font-bold ${colorClass}`}>
                        {value}%
                    </p>
                    {growth !== null && (
                        <div className="flex items-center mt-2">
                            {renderTrendIcon(parseFloat(growth))}
                            <span className={`text-xs ml-1 ${getGrowthColorClass(growth)}`}>
                                {Math.abs(parseFloat(growth)).toFixed(2)}% vs 전년
                            </span>
                        </div>
                    )}
                </CardBody>
            </Card>
        );
    };

    const currentRatio = calculateRatio(latestData["영업이익"], latestData["매출액"]);
    const previousRatio = previousData ? calculateRatio(previousData["영업이익"], previousData["매출액"]) : null;

    return (
        <Card className="w-full mb-4 bg-gradient-to-r from-blue-50 to-indigo-50">
            <CardHeader className="font-bold text-xl">재무 요약 ({latestYear}년)</CardHeader>
            <Divider />
            <CardBody>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    {renderMetricCard("매출액", latestData["매출액"], DollarSign, previousData?.["매출액"])}
                    {renderMetricCard("영업이익", latestData["영업이익"], BarChart2, previousData?.["영업이익"])}
                    {renderMetricCard("당기순이익", latestData["당기순이익"], PieChart, previousData?.["당기순이익"])}
                    {renderRatioCard("영업이익률", currentRatio, previousRatio)}
                </div>
            </CardBody>
        </Card>
    );
};

export default SummaryDashboard;