// src/components/MultiStateButton.tsx
import styles from "css/MultiStateButton.module.css";

interface MultiStateButtonProps {
  activeIndex: number;
  buttonLabels: string[];
  onClick: React.Dispatch<React.SetStateAction<number>>;
}

const MultiStateButton: React.FC<MultiStateButtonProps> =
  ({ activeIndex, buttonLabels, onClick }) => {

  return (
    <ul className={styles.multiStateButton}>
      {[...Array(buttonLabels.length).keys()].map((i) => {
        const isActiveButton = activeIndex === i;
        return (
          <li
            className={isActiveButton ? styles.active : ""}
            onClick={() => onClick(i)}
            key={i}
          >
            {buttonLabels[i]}
          </li>
        );
      })}
    </ul>
  );
};

export default MultiStateButton;