import React from 'react';
import { View, Text } from 'react-native';
import { useRoute, RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../navigation/types';

type StockScreenRouteProp = RouteProp<RootStackParamList, 'Stock'>;

const StockScreen = () => {
    const route = useRoute<StockScreenRouteProp>();
    const { stockId, symbol, name } = route.params;

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', padding: 16 }}>
            <Text style={{ fontSize: 24, fontWeight: 'bold' }}>{symbol}</Text>
            <Text style={{ fontSize: 18, color: 'gray' }}>{name}</Text>
            <Text style={{ marginTop: 20 }}>Stock ID: {stockId}</Text>
            {/* Additional stock information can be fetched and displayed here */}
        </View>
    );
};

export default StockScreen;
