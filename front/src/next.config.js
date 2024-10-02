const withTM = require('next-transpile-modules')(['@nextui-org/ripple', '@nextui-org/tooltip']); // 변환할 모듈 추가

module.exports = withTM({
    reactStrictMode: true,
});
