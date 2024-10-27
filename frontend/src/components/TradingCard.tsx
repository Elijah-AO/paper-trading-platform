import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';

type TradingCardProps = {
  stockName: string;
  stockId: string;
  quantity: number;
  latestPrice?: number;
  timestamp?: string;
  onPress: () => void;
};

const TradingCard = ({ stockName, stockId, quantity, latestPrice, timestamp, onPress }: TradingCardProps) => {
  return (
    <TouchableOpacity onPress={onPress} style={{ margin: 10, padding: 15, borderWidth: 1, borderRadius: 8 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>{stockName}</Text>
      <Text>Quantity: {quantity}</Text>
      {latestPrice !== undefined && <Text>Latest Price: ${latestPrice.toFixed(2)}</Text>}
      {timestamp && <Text>Last Updated: {new Date(timestamp).toLocaleString()}</Text>}
    </TouchableOpacity>
  );
};

export default TradingCard;
