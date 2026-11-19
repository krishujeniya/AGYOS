---
name: upgrading-expo
description: "Upgrade Expo SDK versions safely. Use when updating an Expo project and checking breaking changes, package compatibility, native configuration, and platform builds."
risk: safe
source: "https://github.com/expo/skills/tree/main/plugins/upgrading-expo"
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "upgrading-expo"
sections[18]:
  - "\n"
  - "# Upgrading Expo\n\n"
  - "## Overview\n\nUpgrade Expo SDK versions safely. Use when updating an Expo project and checking breaking changes, package compatibility, native configuration, and platform builds.\n\n"
  - "## When to Use This Skill\n\nUse this skill when you need to upgrade Expo SDK versions.\n\nUse this skill when:\n- Upgrading to a new Expo SDK version\n- Handling breaking changes between SDK versions\n- Updating dependencies for compatibility\n- Migrating deprecated APIs to new versions\n- Preparing apps for new Expo features\n\n"
  - "## Instructions\n\nThis skill guides you through upgrading Expo SDK versions:\n\n1. **Pre-Upgrade Planning**: Review release notes and breaking changes\n2. **Dependency Updates**: Update packages for SDK compatibility\n3. **Configuration Migration**: Update app.json and configuration files\n4. **Code Updates**: Migrate deprecated APIs to new versions\n5. **Testing**: Verify app functionality after upgrade\n\n"
  - "## Upgrade Process\n\n"
  - "### 1. Pre-Upgrade Checklist\n\n- Review Expo SDK release notes\n- Identify breaking changes affecting your app\n- Check compatibility of third-party packages\n- Backup current project state\n- Create a feature branch for the upgrade\n\n"
  - "### 2. Update Expo SDK\n\n```bash\n# Update Expo CLI\nnpm install -g expo-cli@latest\n\n# Upgrade Expo SDK\nnpx expo install expo@latest\n\n# Update all Expo packages\nnpx expo install --fix\n```\n\n"
  - "### 3. Handle Breaking Changes\n\n- Review migration guides for breaking changes\n- Update deprecated API calls\n- Modify configuration files as needed\n- Update native dependencies if required\n- Test affected features thoroughly\n\n"
  - "### 4. Update Dependencies\n\n```bash\n# Check for outdated packages\nnpx expo-doctor\n\n# Update packages to compatible versions\nnpx expo install --fix\n\n# Verify compatibility\nnpx expo-doctor\n```\n\n"
  - "### 5. Testing\n\n- Test core app functionality\n- Verify native modules work correctly\n- Check for runtime errors\n- Test on both iOS and Android\n- Verify app store builds still work\n\n"
  - "## Common Issues\n\n"
  - "### Dependency Conflicts\n\n- Use `expo install` instead of `npm install` for Expo packages\n- Check package compatibility with new SDK version\n- Resolve peer dependency warnings\n\n"
  - "### Configuration Changes\n\n- Update `app.json` for new SDK requirements\n- Migrate deprecated configuration options\n- Update native configuration files if needed\n\n"
  - "### Breaking API Changes\n\n- Review API migration guides\n- Update code to use new APIs\n- Test affected features after changes\n\n"
  - "## Best Practices\n\n- Always upgrade in a feature branch\n- Test thoroughly before merging\n- Review release notes carefully\n- Update dependencies incrementally\n- Keep Expo CLI updated\n- Use `expo-doctor` to verify setup\n\n"
  - "## Resources\n\nFor more information, see the [source repository](https://github.com/expo/skills/tree/main/plugins/upgrading-expo).\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
