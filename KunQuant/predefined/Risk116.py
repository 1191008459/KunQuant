from KunQuant.Op import *
from KunQuant.ops import *

class AllData:
    def __init__(self, open: OpBase,
     close: OpBase = None, 
     high: OpBase = None,
     low: OpBase = None, 
     volume: OpBase = None, 
     amount: OpBase = None, 
     vwap: OpBase = None,
     LowExRet: OpBase = None,
     Preclose: OpBase = None,


     
     ) -> None:
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.amount = amount
        self.LowExRet = LowExRet
        self.Preclose = Preclose

        if vwap is None:
            self.vwap = Div(self.amount, AddConst(self.volume, 0.0000001))
        else:
            self.vwap = vwap
        self.returns = returns(close)

def stddev(v: OpBase, window: int) -> OpBase:
    return WindowedStddev(v, window)

def returns(v: OpBase) -> OpBase:
    prev1 = BackRef(v, 1)
    return SubConst(Div(v, prev1), 1.0)

def ts_argmax(v: OpBase, window: int) -> OpBase:
    return TsArgMax(v, window)

def ts_argmin(v: OpBase, window: int) -> OpBase:
    return TsArgMin(v, window)

def ts_rank(v: OpBase, window: int) -> OpBase:
    return TsRank(v, window)

def ts_sum(v: OpBase, window: int) -> OpBase:
    return WindowedSum(v, window)

def ts_min(v: OpBase, window: int) -> OpBase:
    return WindowedMin(v, window)

def ts_max(v: OpBase, window: int) -> OpBase:
    return WindowedMax(v, window)

def correlation(v1: OpBase, v2: OpBase, window: int) -> OpBase:
    return WindowedCorrelation(v1, window, v2)

def delta(v1: OpBase, window: int = 1) -> OpBase:
    return Sub(v1, BackRef(v1, window))

def x_to_ts_mean(v1:OpBase,window:int)->OpBase:
    return Div(v1,WindowedAvg(v1,window))

def x_to_ts_max(v1:OpBase,window:int)->OpBase:
    return Div(v1,WindowedMax(v1,window))

def x_to_ts_min(v1:OpBase,window:int)->OpBase:
    return Div(v1,WindowedMin(v1,window))

def ts_ir(v1:OpBase,window:int)->OpBase:
    return Div(WindowedAvg(v1,window),WindowedStddev(v1,window))

def rank(v: OpBase)-> OpBase:
    return Rank(v)

def sign(v: OpBase)-> OpBase:
    return Sign(v)

def covariance(v: OpBase, v2: OpBase, window: int) -> OpBase:
    return WindowedCovariance(v, window, v2)

def sma(v: OpBase, window: int) -> OpBase:
    return WindowedAvg(v, window)

def bool_to_10(v: OpBase) -> OpBase:
    return Select(v, ConstantOp(1), ConstantOp(0))

scale = Scale

delay = BackRef
decay_linear = DecayLinear

def Risk001(self: AllData):
    inner = self.close
    return Sqrt(WindowedAvg(inner,60))
def Risk002(self: AllData):
    amount = self.amount
    preclose = self.Preclose
    lowexret = self.LowExRet
    out1 = Div(lowexret,amount)
    out2 = Rank(x_to_ts_min(out1,244))
    out3 = WindowedStddev(Mean(out2,preclose),488)
    return out3 


def Risk003(self: AllData):
    inner = self.close
    return WindowedProduct(x_to_ts_max(inner,10),122)

all_risk = [Risk001,Risk002,Risk003
    ]