import { useRouter } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import { listSpearheads } from '../src/db/queries';
import type { SpearheadSummary } from '../src/db/types';
import { colors } from '../src/theme';

export default function SpearheadListScreen() {
  const db = useSQLiteContext();
  const router = useRouter();
  const [spearheads, setSpearheads] = useState<SpearheadSummary[]>([]);
  const [query, setQuery] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        const rows = await listSpearheads(db);
        if (!cancelled) {
          setSpearheads(rows);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Failed to load armies');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [db]);

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    if (!needle) {
      return spearheads;
    }
    return spearheads.filter(
      (spearhead) =>
        spearhead.name.toLowerCase().includes(needle) ||
        spearhead.factionName.toLowerCase().includes(needle),
    );
  }, [spearheads, query]);

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={colors.accent} size="large" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centered}>
        <Text style={styles.error}>{error}</Text>
      </View>
    );
  }

  return (
    <ScrollView
      contentContainerStyle={styles.content}
      keyboardShouldPersistTaps="handled"
    >
      <Text style={styles.heading}>Choose a Spearhead</Text>
      <Text style={styles.subheading}>
        Tap an army to view roster, weapons, and abilities.
      </Text>

      <Pressable
        accessibilityRole="button"
        onPress={() => router.push('/rules')}
        style={({ pressed }) => [
          styles.rulesButton,
          pressed && styles.rulesButtonPressed,
        ]}
      >
        <Text style={styles.rulesButtonTitle}>Rules reference</Text>
        <Text style={styles.rulesButtonSubtitle}>
          Deployment, phases, core abilities, and more
        </Text>
      </Pressable>

      <TextInput
        value={query}
        onChangeText={setQuery}
        placeholder="Search by spearhead or faction"
        placeholderTextColor={colors.textMuted}
        autoCorrect={false}
        autoCapitalize="none"
        clearButtonMode="while-editing"
        accessibilityLabel="Search spearheads"
        style={styles.search}
      />

      <View style={styles.list}>
        {filtered.map((spearhead) => (
          <Pressable
            key={spearhead.slug}
            accessibilityRole="button"
            onPress={() =>
              router.push({
                pathname: '/spearhead/[slug]',
                params: { slug: spearhead.slug },
              })
            }
            style={({ pressed }) => [
              styles.button,
              pressed && styles.buttonPressed,
            ]}
          >
            <Text style={styles.buttonTitle}>{spearhead.name}</Text>
            <Text style={styles.buttonSubtitle}>{spearhead.factionName}</Text>
          </Pressable>
        ))}
        {filtered.length === 0 ? (
          <Text style={styles.empty}>No spearheads match “{query.trim()}”.</Text>
        ) : null}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: 20,
    paddingBottom: 40,
    gap: 12,
  },
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.bg,
    padding: 24,
  },
  heading: {
    color: colors.text,
    fontSize: 28,
    fontWeight: '800',
    letterSpacing: 0.3,
  },
  subheading: {
    color: colors.textMuted,
    fontSize: 15,
    lineHeight: 22,
    marginBottom: 8,
  },
  rulesButton: {
    backgroundColor: colors.accent,
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 18,
  },
  rulesButtonPressed: {
    opacity: 0.88,
  },
  rulesButtonTitle: {
    color: colors.accentText,
    fontSize: 18,
    fontWeight: '700',
  },
  rulesButtonSubtitle: {
    color: colors.accentText,
    opacity: 0.85,
    fontSize: 14,
    marginTop: 4,
  },
  search: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 12,
    color: colors.text,
    fontSize: 16,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginBottom: 4,
  },
  list: {
    gap: 12,
  },
  empty: {
    color: colors.textMuted,
    fontSize: 15,
    lineHeight: 22,
    paddingVertical: 8,
  },
  button: {
    backgroundColor: colors.surfaceRaised,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 18,
  },
  buttonPressed: {
    backgroundColor: colors.accent,
    borderColor: colors.accent,
  },
  buttonTitle: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '700',
  },
  buttonSubtitle: {
    color: colors.textMuted,
    fontSize: 14,
    marginTop: 4,
  },
  error: {
    color: '#e8a0a0',
    textAlign: 'center',
    fontSize: 16,
  },
});
