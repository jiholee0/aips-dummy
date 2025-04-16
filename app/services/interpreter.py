import re
from app.utils.model_enum import ModelType, ChemicalType
from typing import Dict
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Interpreter:
    @staticmethod
    def interpret(content: bytes) -> Dict:
        """
        파일 내용을 기반으로 input_type을 추론하고,
        model_type과 chemical_type을 결정하는 로직.
        """
        if not content:
            logger.warning("[Interpreter] 파일 내용이 비어 있음")
            return {"valid": False, "reason": "파일 내용이 비어 있습니다.", "type": {}}

        text = content.decode("utf-8", errors="ignore").strip()
        logger.info("[Interpreter] content 길이: %d bytes", len(text))

        # input_type 추론
        if text.startswith("MJ") or "M  END" in text:
            # MOL 또는 MOL_3D 구분
            lines = text.strip().splitlines()
            atom_lines = [line for line in lines if re.match(r"^\\s*-?\\d+\\.\\d+\\s+-?\\d+\\.\\d+\\s+-?\\d+\\.\\d+", line)]
            has_z_coordinate = all(len(line.split()) >= 4 for line in atom_lines)
            if has_z_coordinate:
                input_type = "mol_3d"
            else:
                input_type = "mol"
        elif text.startswith("ATOM") and "XYZ" in text.upper():
            input_type = "mol_3d"
        elif all(c.isalnum() or c in "@+=#()[]\\/.-" for c in text):
            input_type = "smiles"
        else:
            logger.warning("[Interpreter] input_type 판별 실패")
            return {"valid": False, "reason": "input_type을 판별할 수 없습니다.", "type": {}}

        model_type_map = {
            "mol": ModelType.GNN,
            "mol_3d": ModelType.ML,
            "smiles": ModelType.NLP
        }

        model_type = model_type_map[input_type]

        result = {
            "valid": True,
            "type": {
                "input_type": input_type,
                "model_type": model_type.value,
                "chemical_type": ChemicalType.GENERAL.value
            }
        }

        logger.info(f"[Interpreter] 해석 결과: {result}")
        return result
