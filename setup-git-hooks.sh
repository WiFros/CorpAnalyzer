#!/bin/bash

# .githooks 디렉토리 생성
mkdir -p .githooks

# commit-msg 훅 생성 또는 업데이트
cat > .githooks/commit-msg << 'EOL'
#!/bin/bash

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# 커밋 메시지 패턴 정의 (예: "type: subject")
pattern="^(feat|fix|docs|style|refactor|test|chore|update|init): .{1,50}$"

if ! [[ "$commit_msg" =~ $pattern ]]; then
    echo "오류: 커밋 메시지가 지정된 규칙을 따르지 않습니다."
    echo "커밋 메시지는 다음 형식을 따라야 합니다: type: subject"
    echo "허용되는 타입: feat, fix, docs, style, refactor, test, chore, init, update"
    echo "제목(subject)은 50자를 넘지 않아야 합니다."
    exit 1
fi
EOL

# post-merge 훅 생성 또는 업데이트
cat > .githooks/post-merge << 'EOL'
#!/bin/bash

# 현재 스크립트의 경로를 가져옵니다.
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 프로젝트 루트 디렉토리로 이동합니다.
cd "$SCRIPT_PATH/.."

# setup-git-hooks.sh 스크립트를 실행합니다.
bash setup-git-hooks.sh
EOL

# 훅 파일들에 실행 권한 부여
chmod +x .githooks/*

# Git 설정을 변경하여 .githooks 디렉토리를 사용하도록 설정
git config core.hooksPath .githooks

echo "Git hooks 설정이 완료되었습니다."
echo ".githooks 디렉토리가 생성되었으며, commit-msg와 post-merge 훅이 추가/업데이트되었습니다."
echo "Git 설정이 변경되어 .githooks 디렉토리를 사용합니다."
echo "이제 pull을 받을 때마다 자동으로 Git hooks가 업데이트됩니다."