import { Stack } from 'expo-router';
import { SQLiteProvider } from 'expo-sqlite';
import { StatusBar } from 'expo-status-bar';

import { colors } from '../src/theme';

export default function RootLayout() {
  return (
    <SQLiteProvider
      databaseName="spearhead.sqlite"
      assetSource={{
        assetId: require('../assets/databases/spearhead.sqlite'),
      }}
      onError={(error) => console.error('SQLiteProvider error', error)}
    >
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: colors.surface },
          headerTintColor: colors.text,
          headerTitleStyle: { fontWeight: '700' },
          contentStyle: { backgroundColor: colors.bg },
        }}
      >
        <Stack.Screen name="index" options={{ title: 'Spearhead Armies' }} />
        <Stack.Screen
          name="spearhead/[slug]"
          options={{ title: 'Army Details' }}
        />
      </Stack>
    </SQLiteProvider>
  );
}
