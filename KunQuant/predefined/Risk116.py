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
     ExRet: OpBase = None,
     LowPct: OpBase = None,
     TR: OpBase = None,
     CloseOpenPct: OpBase = None,
     HighExRet: OpBase = None,
     HighLowPct: OpBase = None,
     VwapPct: OpBase = None,
     HighPct: OpBase = None,
     ) -> None:
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.amount = amount
        self.LowExRet = LowExRet
        self.Preclose = Preclose
        self.ExRet = ExRet
        self.LowPct = LowPct
        self.TR = TR
        self.CloseOpenPct = CloseOpenPct
        self.HighExRet = HighExRet
        self.HighLowPct = HighLowPct
        self.VwapPct = VwapPct
        self.HighPct = HighPct
        if vwap is None:
            self.vwap = Div(self.amount, AddConst(self.volume, 0.0000001))
        else:
            self.vwap = vwap
        self.returns = returns(close)

def stddev(v: OpBase, window: int) -> OpBase:
    return WindowedStddev(v, window)

def ts_corr(v1: OpBase, v2: OpBase, window: int) -> OpBase:
    return WindowedCorrelation(v1, window, v2)

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

def Inv(v: OpBase) -> OpBase:
    return Div(ConstantOp(1), v)

def ts_maxmin(v1: OpBase, window: int) -> OpBase:
    return Sub(WindowedMax(v1,window),WindowedMin(v1,window))

def ts_maxmin_norm(v1: OpBase, window: int) -> OpBase:
    return Div(Sub(v1, WindowedMin(v1,window)), ts_maxmin(v1,window))

def ts_delta_perc(v1: OpBase, window: int) -> OpBase:
    return Div(Sub(v1, BackRef(v1, window)), Abs(BackRef(v1, window)))

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
    out3 = WindowedStddev(DivConst(Add(out2,preclose), 2),488)
    return out3 



def Risk003(self: AllData):
    inner = self.close
    return WindowedProduct(x_to_ts_max(inner,10),122)

def Risk004(self: AllData):
    ExRet = self.ExRet
    LowPct = self.LowPct
    return WindowedCorrelation(ExRet,244,LowPct)

def Risk005(self: AllData):
    tr = self.TR
    COP = self.CloseOpenPct
    out1 = Sqrt(Sub(tr,COP))
    return WindowedSum(out1,122)

def Risk006(self: AllData):
    HighExRet = self.HighExRet
    
    out1 = Inv(ts_ir(Pow(HighExRet, ConstantOp(0.333)),244))
    return Rank(out1)

def Risk007(self: AllData):
    VWAP = self.vwap
    High = self.high
    out1 = Inv(Div(High,MulConst(ts_maxmin(VWAP, 366), -1)))
    return out1

def Risk008(self: AllData):
    low = self.low
    tr = self.TR
    out1 = ts_ir(Log(Sub(low,Pow(tr,ConstantOp(2.0)))),122)
    return out1 

def Risk010(self: AllData):
    High = self.high
    return ts_ir(High,60)

def Risk014(self: AllData):
    highlowpct = self.HighLowPct
    out = Sqrt(WindowedSum(Log(MulConst(highlowpct, 488.0)),244))
    return out 

def Risk017(self: AllData):
    close = self.close
    out = ts_min(ts_maxmin(Sqrt(close),20),244)
    return out 

def Risk036(self: AllData):
    amt = self.amount
    return ts_min(amt,366)

def Risk016(self: AllData):
    low = scale(self.low)
    out = stddev(low, 244)
    open = self.open
    return  Div(Sqrt(open),out) 

def Risk022(self: AllData):
    low = self.low
    high = self.high
    return ts_corr(high,low,244)

def Risk018(self: AllData):
    exret = self.ExRet
    out = scale(Pow(exret, ConstantOp(0.333)))
    return ts_sum(out, 488)

def Risk013(self: AllData):
    vwap_ret = self.VwapPct
    Vwap = self.vwap
    preclose = self.Preclose
    out = WindowedSum(Sqrt(Mul(Sub(vwap_ret, Vwap),preclose)),122)
    return Div(ConstantOp(366),out)

def Risk019(self: AllData):
    vwap_ret = self.VwapPct
    LowExRet = self.LowExRet
    return WindowedAvg(Add(LowExRet,vwap_ret),60)


def Risk020(self: AllData):
    preclose = self.Preclose
    open = self.open
    return WindowedLinearRegressionSlope(preclose,122,scale(open))

def Risk029(self: AllData):
    amount = self.amount
    tr = self.TR
    return WindowedAvg(Div(Pow(amount,ConstantOp(0.333)),tr),60)

def Risk031(self: AllData):
    highpct = self.HighPct
    highExRet = self.HighExRet
    return Abs(WindowedLinearRegressionSlope(highpct, 60, highExRet))


all_risk = [Risk001,Risk002,Risk003,Risk004,Risk005,Risk006,
          Risk007,Risk008,Risk010,Risk014,
            Risk017,Risk036,Risk016,Risk022,Risk018,
            Risk013,Risk019,Risk020,Risk029,Risk031
            
            ]
