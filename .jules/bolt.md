## 2023-10-27 - Bun.stripANSI 제거 및 node:util 도입

**학습 내용:**
- Bun v1.2.14 기준으로 `Bun.stripANSI` 메서드가 더 이상 내장 API로 제공되지 않아 이를 사용하는 테스트들이 런타임 오류(TypeError: Bun.stripANSI is not a function)로 실패하는 문제를 발견했습니다.
- 이를 해결하기 위해 Node 표준 유틸리티인 `node:util` 모듈의 `stripVTControlCharacters`를 사용해 동일한 동작을 수행하도록 변경했습니다.
- 내장 런타임 API에 의존할 때 버전 간 브레이킹 체인지(Breaking change)로 인해 전체 빌드가 깨질 수 있으므로, Node 표준 라이브러리가 제공하는 동등한 API를 우선 사용하는 것이 유지보수에 더 유리하다는 점을 확인했습니다.

**적용 계획:**
- 다음번 최적화나 기능 개발 시, 특정 런타임 환경(Bun, Deno 등)에 종속적인 API를 사용하기 전에 Node.js 내장 모듈(`node:util`, `node:fs` 등)로 대체 가능한지 우선 검토합니다.
- 외부 의존성 없이 표준 모듈로 처리 가능한 문자열 가공/정제(Sanitization) 작업에는 가급적 표준 모듈을 활용하여 런타임 독립성을 확보합니다.
