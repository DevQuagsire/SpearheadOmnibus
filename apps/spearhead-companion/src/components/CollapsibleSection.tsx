import { useState, type ReactNode } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { colors } from '../theme';

export function CollapsibleSection({
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

const styles = StyleSheet.create({
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
});
