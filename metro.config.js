// // const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');

// // /**
// //  * Metro configuration
// //  * https://metrobundler.dev/docs/configuration
// //  *
// //  * @type {import('metro-config').MetroConfig}
// //  */
// // const config = {};

// // module.exports = mergeConfig(getDefaultConfig(__dirname), config);

// // metro.config.js
// const { getDefaultConfig } = require('@expo/metro-config');

// module.exports = (async () => {
//   const config = await getDefaultConfig(__dirname);

//   config.resolver.experimentalImportSupport = true; // Enable the experimental require.context feature

//   return config;
// })();

const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');

/**
 * Metro configuration
 * https://reactnative.dev/docs/metro
 *
 * @type {import('@react-native/metro-config').MetroConfig}
 */
const config = {};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);