// src/components/TradingCard.tsx
import React from 'react';
import { Box, Text, Pressable, VStack } from 'native-base';

type TradingCardProps = {
  stockName: string;
  stockId: string;
  quantity: number;
  onPress: () => void;
};

const TradingCard: React.FC<TradingCardProps> = ({ stockName, stockId, quantity, onPress }) => {
  return (
    <Pressable onPress={onPress}>
      {({ isPressed }) => (
        <Box
          bg={isPressed ? "coolGray.200" : "white"}
          p="4"
          rounded="md"
          shadow={2}
          borderWidth="1"
          borderColor="coolGray.300"
          mb="2"
          width="90%"
          maxW="290px"
        >
          <VStack space={2}>
            <Text fontSize="lg" fontWeight="bold">{stockName}</Text>
            <Text fontSize="sm" color="gray.500">ID: {stockId}</Text>
            <Text fontSize="md">Quantity: {quantity}</Text>
          </VStack>
        </Box>
      )}
    </Pressable>
  );
};

export default TradingCard;
