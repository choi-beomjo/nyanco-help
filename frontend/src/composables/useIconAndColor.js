export function useIconAndColor() {
    const getPropertyColor = (property) => {
        const propertyColors = {
            red: "#ff4d4d",
            white: "#FFFFFF",
            metal: "#b0c4de",
            blue: "#007bff",
            fly: "#28a745",
            black: "#333",
            angel: "#ffeb99",
            navy: "#001f3f",
            zombie: "#800080",
            alien: "#87ceeb",
        };
        return propertyColors[property.toLowerCase()] || "property-default";
      };
      const getSkillIcon = (skill) => {
        const skillIcons = {
          "멈추기": `<i class="fas fa-clock"></i>`, // 🕰️ 시계
          "멈추기 무효": `
              <i class="fas fa-clock"></i>
              <i class="fas fa-ban margin-left: 5px"></i>
          `, // 🕰️+🚫 (시계+금지)
          "엄청 강하다": `<i class="fas fa-hand-rock"></i>`, // ✊ 권투 글러브
          "방어력 증가": `<i class="fas fa-shield-alt"></i>`, // 🛡️ 방패
          "파동": `<i class="fas fa-wave-square"></i>`, // 🌊 파동
          "독 데미지": `<i class="fas fa-skull-crossbones"></i>`, // ☠️ 독
          "날려버린다": `<i class="fas fa-wind"></i>`, // 💨 바람
          "공격력 업":`
              <i class="fas fa-hammer"></i>
              <i class="fas fa-arrow-up margin-left: 5px"></i>
          `,
          "느리게 한다":`
            <i class="fas fa-running"></i>
            <i class="fas fa-arrow-down margin-left: 5px"></i>
          `,
        };
        return skillIcons[skill] ||  `<i class="fas fa-question-circle"></i>`; // ❓ 기본 아이콘
      };

      const getTextColor = (property) => {
        const backgroundColor = getPropertyColor(property);
        const brightness = parseInt(backgroundColor.replace("#", ""), 16); // 색상 밝기 계산
        return brightness > 0xffffff / 2 ? "#000" : "#fff"; // 밝으면 검은색, 어두우면 흰색
      };
      return { getSkillIcon, getPropertyColor, getTextColor };
}