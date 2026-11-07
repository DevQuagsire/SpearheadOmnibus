import { Stack, useLocalSearchParams } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { useEffect, useState, type ReactNode } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { getSpearheadDetail } from '../../src/db/queries';
import type {
  AbilityRow,
  RosterUnit,
  SpearheadDetail,
  WeaponRow,
} from '../../src/db/types';
import { colors } from '../../src/theme';

function CollapsibleSection({
  title,
  count,
  defaultExpanded = true,
  children,
}: {
  title: string;
  count?: number;
  defaultExpanded?: boolean;
  children: ReactNode;
}) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const countLabel = count != null ? ` (${count})` : '';

  return (
    <View style={styles.group}>
      <Pressable
        accessibilityRole="button"
        accessibilityState={{ expanded }}
        onPress={() => setExpanded((value) => !value)}
        style={({ pressed }) => [
          styles.sectionHeader,
          pressed && styles.sectionHeaderPressed,
        ]}
      >
        <Text style={styles.groupTitle}>
          {title}
          {countLabel}
        </Text>
        <Text style={styles.chevron}>{expanded ? '▾' : '▸'}</Text>
      </Pressable>
      {expanded ? <View style={styles.sectionBody}>{children}</View> : null}
    </View>
  );
}

function AbilityCard({ ability }: { ability: AbilityRow }) {
  return (
    <View style={styles.abilityCard}>
      <Text style={styles.abilityName}>{ability.name}</Text>
      <Text style={styles.abilityTrigger}>{ability.trigger}</Text>
      <Text style={styles.abilityEffect}>{ability.effect}</Text>
    </View>
  );
}

function WeaponRowView({ weapon }: { weapon: WeaponRow }) {
  const range =
    weapon.kind === 'ranged' && weapon.rangeInches != null
      ? `${weapon.rangeInches}"`
      : 'Melee';
  const abilityText =
    weapon.abilities.length > 0
      ? ` · ${weapon.abilities.join(', ')}`
      : '';

  return (
    <View style={styles.weaponRow}>
      <Text style={styles.weaponName}>{weapon.name}</Text>
      <Text style={styles.weaponStats}>
        {range} · A {weapon.attacks} · Hit {weapon.hit}+ · Wound {weapon.wound}+
        · Rend {weapon.rend} · Dmg {weapon.damage}
        {abilityText}
      </Text>
    </View>
  );
}

function UnitSection({ unit }: { unit: RosterUnit }) {
  const [expanded, setExpanded] = useState(true);
  const badges = [
    unit.isGeneral ? 'General' : null,
    unit.isReinforcement ? 'Reinforcement' : null,
    `${unit.modelCount} model${unit.modelCount === 1 ? '' : 's'}`,
  ].filter(Boolean);

  return (
    <View style={styles.unitCard}>
      <Pressable
        accessibilityRole="button"
        accessibilityState={{ expanded }}
        onPress={() => setExpanded((value) => !value)}
        style={({ pressed }) => [
          styles.unitHeader,
          pressed && styles.sectionHeaderPressed,
        ]}
      >
        <View style={styles.unitHeaderText}>
          <Text style={styles.unitName}>{unit.unitTypeName}</Text>
          <View style={styles.badgeRow}>
            {badges.map((badge) => (
              <View key={String(badge)} style={styles.badge}>
                <Text style={styles.badgeText}>{badge}</Text>
              </View>
            ))}
          </View>
        </View>
        <Text style={styles.chevron}>{expanded ? '▾' : '▸'}</Text>
      </Pressable>

      {expanded ? (
        <View style={styles.unitBody}>
          <Text style={styles.statLine}>
            Control {unit.control} · Health {unit.health} · Move {unit.move}" ·
            Save {unit.save}+
          </Text>

          {unit.keywords.length > 0 ? (
            <Text style={styles.keywords}>
              Keywords:{' '}
              {unit.keywords.map((keyword) => keyword.toUpperCase()).join(', ')}
            </Text>
          ) : null}

          <Text style={styles.sectionLabel}>Weapons</Text>
          {unit.weapons.map((weapon) => (
            <WeaponRowView key={`${unit.id}-${weapon.slug}`} weapon={weapon} />
          ))}

          {unit.abilities.length > 0 ? (
            <>
              <Text style={styles.sectionLabel}>Unit Abilities</Text>
              {unit.abilities.map((ability) => (
                <AbilityCard
                  key={`${unit.id}-${ability.slug}`}
                  ability={ability}
                />
              ))}
            </>
          ) : null}
        </View>
      ) : null}
    </View>
  );
}

function AbilityGroup({
  title,
  abilities,
}: {
  title: string;
  abilities: AbilityRow[];
}) {
  if (abilities.length === 0) {
    return null;
  }

  return (
    <CollapsibleSection title={title} count={abilities.length}>
      {abilities.map((ability) => (
        <AbilityCard key={ability.slug} ability={ability} />
      ))}
    </CollapsibleSection>
  );
}

export default function SpearheadDetailScreen() {
  const { slug } = useLocalSearchParams<{ slug: string }>();
  const db = useSQLiteContext();
  const [detail, setDetail] = useState<SpearheadDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    if (!slug) {
      setError('Missing spearhead slug');
      setLoading(false);
      return;
    }

    (async () => {
      try {
        const row = await getSpearheadDetail(db, slug);
        if (!cancelled) {
          if (!row) {
            setError(`No spearhead found for "${slug}"`);
          } else {
            setDetail(row);
          }
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Failed to load army');
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
  }, [db, slug]);

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={colors.accent} size="large" />
      </View>
    );
  }

  if (error || !detail) {
    return (
      <View style={styles.centered}>
        <Text style={styles.error}>{error ?? 'Army not found'}</Text>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen options={{ title: detail.name }} />
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.faction}>{detail.factionName}</Text>
        <Text style={styles.title}>{detail.name}</Text>

        <CollapsibleSection title="Roster" count={detail.units.length}>
          {detail.units.map((unit) => (
            <UnitSection key={unit.id} unit={unit} />
          ))}
        </CollapsibleSection>

        <AbilityGroup title="Battle Traits" abilities={detail.battleTraits} />
        <AbilityGroup
          title="Regiment Abilities"
          abilities={detail.regimentAbilities}
        />
        <AbilityGroup title="Enhancements" abilities={detail.enhancements} />
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: 20,
    paddingBottom: 48,
    gap: 18,
  },
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.bg,
    padding: 24,
  },
  faction: {
    color: colors.accent,
    fontSize: 13,
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: 1.2,
  },
  title: {
    color: colors.text,
    fontSize: 30,
    fontWeight: '800',
    marginTop: -8,
  },
  group: {
    gap: 10,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 6,
    paddingHorizontal: 4,
    borderRadius: 8,
  },
  sectionHeaderPressed: {
    backgroundColor: colors.surface,
  },
  sectionBody: {
    gap: 10,
  },
  groupTitle: {
    color: colors.text,
    fontSize: 20,
    fontWeight: '700',
    flex: 1,
  },
  chevron: {
    color: colors.textMuted,
    fontSize: 18,
    fontWeight: '700',
    marginLeft: 12,
  },
  unitCard: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 12,
    overflow: 'hidden',
  },
  unitHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    padding: 14,
    gap: 8,
  },
  unitHeaderText: {
    flex: 1,
    gap: 8,
  },
  unitBody: {
    paddingHorizontal: 14,
    paddingBottom: 14,
    gap: 8,
  },
  unitName: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '700',
  },
  badgeRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  badge: {
    backgroundColor: colors.chip,
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 4,
  },
  badgeText: {
    color: colors.textMuted,
    fontSize: 12,
    fontWeight: '600',
  },
  statLine: {
    color: colors.text,
    fontSize: 14,
  },
  keywords: {
    color: colors.textMuted,
    fontSize: 13,
  },
  sectionLabel: {
    color: colors.accent,
    fontSize: 13,
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: 0.8,
    marginTop: 6,
  },
  weaponRow: {
    gap: 2,
  },
  weaponName: {
    color: colors.text,
    fontSize: 15,
    fontWeight: '600',
  },
  weaponStats: {
    color: colors.textMuted,
    fontSize: 13,
    lineHeight: 18,
  },
  abilityCard: {
    backgroundColor: colors.surfaceRaised,
    borderRadius: 10,
    padding: 12,
    gap: 4,
  },
  abilityName: {
    color: colors.text,
    fontSize: 15,
    fontWeight: '700',
  },
  abilityTrigger: {
    color: colors.accent,
    fontSize: 12,
    fontWeight: '600',
  },
  abilityEffect: {
    color: colors.textMuted,
    fontSize: 14,
    lineHeight: 20,
  },
  error: {
    color: '#e8a0a0',
    textAlign: 'center',
    fontSize: 16,
  },
});
