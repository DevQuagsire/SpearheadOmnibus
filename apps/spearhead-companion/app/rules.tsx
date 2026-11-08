import { useMemo, useState } from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import { CollapsibleSection } from '../src/components/CollapsibleSection';
import {
  sectionSearchText,
  spearheadReferenceSections,
  type ReferenceBlock,
  type ReferenceSection,
} from '../src/data/spearheadReference';
import { colors } from '../src/theme';

function BlockView({ block }: { block: ReferenceBlock }) {
  switch (block.kind) {
    case 'paragraph':
      return <Text style={styles.body}>{block.text}</Text>;
    case 'bullets':
      return (
        <View style={styles.bulletList}>
          {block.items.map((item) => (
            <View key={item} style={styles.bulletRow}>
              <Text style={styles.bulletMark}>•</Text>
              <Text style={styles.body}>{item}</Text>
            </View>
          ))}
        </View>
      );
    case 'ability':
      return (
        <View style={styles.abilityCard}>
          <Text style={styles.abilityName}>{block.name}</Text>
          {block.timing ? (
            <Text style={styles.abilityTrigger}>{block.timing}</Text>
          ) : null}
          {block.declare ? (
            <Text style={styles.body}>
              <Text style={styles.label}>Declare: </Text>
              {block.declare}
            </Text>
          ) : null}
          <Text style={styles.body}>
            <Text style={styles.label}>Effect: </Text>
            {block.effect}
          </Text>
          {block.keywords ? (
            <Text style={styles.keywords}>KEYWORDS {block.keywords}</Text>
          ) : null}
        </View>
      );
    case 'named':
      return (
        <View style={styles.namedCard}>
          <Text style={styles.namedTitle}>{block.name}</Text>
          <Text style={styles.body}>{block.text}</Text>
        </View>
      );
    case 'phases':
      return (
        <View style={styles.phaseRow}>
          {block.phases.map((phase, index) => (
            <View key={phase} style={styles.phaseChipWrap}>
              <View style={styles.phaseChip}>
                <Text style={styles.phaseText}>{phase}</Text>
              </View>
              {index < block.phases.length - 1 ? (
                <Text style={styles.phaseArrow}>→</Text>
              ) : null}
            </View>
          ))}
        </View>
      );
  }
}

function SectionView({ section }: { section: ReferenceSection }) {
  return (
    <CollapsibleSection title={section.title} defaultExpanded={false}>
      {section.blocks.map((block, index) => (
        <BlockView key={`${section.slug}-${index}`} block={block} />
      ))}
    </CollapsibleSection>
  );
}

export default function RulesScreen() {
  const [query, setQuery] = useState('');

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    if (!needle) {
      return spearheadReferenceSections;
    }
    return spearheadReferenceSections.filter((section) =>
      sectionSearchText(section).includes(needle),
    );
  }, [query]);

  return (
    <ScrollView
      contentContainerStyle={styles.content}
      keyboardShouldPersistTaps="handled"
    >
      <Text style={styles.heading}>Spearhead Reference</Text>
      <Text style={styles.subheading}>
        Quick rules from the official Spearhead Reference card.
      </Text>

      <TextInput
        value={query}
        onChangeText={setQuery}
        placeholder="Search rules"
        placeholderTextColor={colors.textMuted}
        autoCorrect={false}
        autoCapitalize="none"
        clearButtonMode="while-editing"
        accessibilityLabel="Search rules"
        style={styles.search}
      />

      <View style={styles.sections}>
        {filtered.map((section) => (
          <SectionView key={section.slug} section={section} />
        ))}
        {filtered.length === 0 ? (
          <Text style={styles.empty}>No rules match “{query.trim()}”.</Text>
        ) : null}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: 20,
    paddingBottom: 48,
    gap: 12,
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
    marginBottom: 4,
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
  sections: {
    gap: 16,
  },
  empty: {
    color: colors.textMuted,
    fontSize: 15,
    lineHeight: 22,
    paddingVertical: 8,
  },
  body: {
    color: colors.textMuted,
    fontSize: 14,
    lineHeight: 20,
    flex: 1,
  },
  label: {
    color: colors.text,
    fontWeight: '700',
  },
  bulletList: {
    gap: 8,
  },
  bulletRow: {
    flexDirection: 'row',
    gap: 8,
    alignItems: 'flex-start',
  },
  bulletMark: {
    color: colors.accent,
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '700',
  },
  abilityCard: {
    backgroundColor: colors.surfaceRaised,
    borderRadius: 10,
    padding: 12,
    gap: 6,
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
  keywords: {
    color: colors.text,
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 0.6,
    textTransform: 'uppercase',
    marginTop: 2,
  },
  namedCard: {
    backgroundColor: colors.surfaceRaised,
    borderRadius: 10,
    padding: 12,
    gap: 4,
  },
  namedTitle: {
    color: colors.text,
    fontSize: 15,
    fontWeight: '700',
  },
  phaseRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: 6,
  },
  phaseChipWrap: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  phaseChip: {
    backgroundColor: colors.chip,
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 6,
  },
  phaseText: {
    color: colors.text,
    fontSize: 12,
    fontWeight: '600',
  },
  phaseArrow: {
    color: colors.textMuted,
    fontSize: 14,
    fontWeight: '700',
  },
});
